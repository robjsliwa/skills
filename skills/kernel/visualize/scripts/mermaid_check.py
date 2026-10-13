#!/usr/bin/env python3
"""Validate every Mermaid block in markdown files with mmdc.

Usage:
  mermaid_check.py [paths...] [--png OUTDIR] [--mmdc CMD] [--jobs N]

Walks the given files and directories (default: current directory) for *.md,
skipping .git, node_modules and .viewer. Each ```mermaid fenced block that is
not nested inside another fence is written to a temp .mmd and rendered with
mmdc. Prints PASS or FAIL per block with file:line and a trimmed parser error.

With --png OUTDIR, renders PNGs into OUTDIR (named <file>-L<line>.png) so you
can open them and look. Without it, renders SVG into a temp dir and discards it.

Exit codes: 0 all pass, 1 any block failed, 2 mmdc or its browser unavailable.

Finding mmdc: --mmdc CMD if given, else `mmdc` on PATH, else
`npx -y -p @mermaid-js/mermaid-cli mmdc`. Finding a browser: puppeteer's own
cache, else PUPPETEER_EXECUTABLE_PATH, else a Chrome or Chromium found on the
system (Playwright installs included). Running as root adds --no-sandbox.
"""

import argparse
import concurrent.futures
import glob
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

SKIP_DIRS = {".git", "node_modules", ".viewer"}
FENCE_RE = re.compile(r"^( {0,3})(`{3,}|~{3,})\s*([^\s`]*)")
UNAVAILABLE_HINTS = (
    "Could not find Chrome",
    "Could not find chrome",
    "Failed to launch the browser",
    "command not found",
    "ENOENT",
    "npm ERR!",
    "Cannot find module",
)


def find_markdown(paths):
    out = []
    for p in paths:
        if os.path.isfile(p):
            if p.endswith(".md"):
                out.append(p)
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for f in sorted(files):
                if f.endswith(".md"):
                    out.append(os.path.join(root, f))
    return out


def extract_blocks(path):
    """Return [(line_number, source)] for top-level mermaid fences."""
    blocks = []
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    fence = None  # (char, length, is_mermaid, start_line, body)
    for i, line in enumerate(lines, start=1):
        m = FENCE_RE.match(line)
        if fence is None:
            if m:
                marker, info = m.group(2), m.group(3).lower()
                fence = (marker[0], len(marker), info == "mermaid", i, [])
            continue
        char, length, is_mermaid, start, body = fence
        stripped = line.strip()
        if (
            m
            and m.group(2)[0] == char
            and len(m.group(2)) >= length
            and stripped == m.group(2)
        ):
            if is_mermaid:
                blocks.append((start, "\n".join(body) + "\n"))
            fence = None
            continue
        body.append(line)
    return blocks


def find_browser():
    env = os.environ.get("PUPPETEER_EXECUTABLE_PATH")
    if env and os.path.exists(env):
        return env
    cache = os.environ.get("PUPPETEER_CACHE_DIR") or os.path.expanduser(
        "~/.cache/puppeteer"
    )
    if os.path.isdir(cache) and os.listdir(cache):
        return None  # puppeteer has its own browser
    patterns = [
        os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-*/*/headless_shell"),
        "/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell",
        os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux/chrome"),
        "/opt/pw-browsers/chromium-*/chrome-linux/chrome",
    ]
    for pat in patterns:
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
        hit = shutil.which(name)
        if hit:
            return hit
    mac = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if os.path.exists(mac):
        return mac
    return None


def mmdc_command(explicit):
    if explicit:
        return shlex.split(explicit)
    if shutil.which("mmdc"):
        return ["mmdc"]
    if shutil.which("npx"):
        return ["npx", "-y", "-p", "@mermaid-js/mermaid-cli", "mmdc"]
    return None


def trim_error(text):
    lines = [l for l in text.splitlines() if l.strip()]
    keep = []
    for l in lines:
        s = l.strip()
        if s.startswith("at ") or "node_modules" in s or s.startswith("Generating"):
            continue
        keep.append(l.rstrip())
    return "\n".join(keep[:6]) or text.strip()[:400]


def render(cmd, puppeteer_cfg, src, out_path, work):
    fd, mmd = tempfile.mkstemp(suffix=".mmd", dir=work)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(src)
    args = cmd + ["-q", "-i", mmd, "-o", out_path, "-p", puppeteer_cfg]
    if out_path.endswith(".png"):
        args += ["-b", "white", "-s", "2"]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        return False, "mmdc timed out after 180s"
    except FileNotFoundError as e:
        return None, str(e)
    output = (r.stderr or "") + (r.stdout or "")
    if r.returncode == 0 and os.path.exists(out_path):
        return True, ""
    if any(h in output for h in UNAVAILABLE_HINTS):
        return None, trim_error(output)
    return False, trim_error(output)


def slug(path, line):
    rel = os.path.relpath(path).replace(os.sep, "_").replace(".md", "")
    rel = re.sub(r"[^A-Za-z0-9_.-]", "-", rel).lstrip("._")
    return f"{rel}-L{line}"


def main():
    ap = argparse.ArgumentParser(description="Validate Mermaid blocks in markdown with mmdc.")
    ap.add_argument("paths", nargs="*", default=["."])
    ap.add_argument("--png", metavar="OUTDIR", help="render PNGs here to look at")
    ap.add_argument("--mmdc", metavar="CMD", help="mmdc command, e.g. 'npx -y @mermaid-js/mermaid-cli'")
    ap.add_argument("--jobs", type=int, default=4, help="parallel renders (default 4)")
    opts = ap.parse_args()

    files = find_markdown(opts.paths)
    work_items = [(f, line, src) for f in files for line, src in extract_blocks(f)]
    if not work_items:
        print(f"No Mermaid blocks found in {len(files)} markdown file(s).")
        return 0

    cmd = mmdc_command(opts.mmdc)
    if cmd is None:
        print("mmdc unavailable: no `mmdc` on PATH and no `npx`. Install Node, or mark diagrams %% unvalidated.")
        return 2

    work = tempfile.mkdtemp(prefix="mermaid-check-")
    try:
        cfg = {"args": ["--no-sandbox"]} if hasattr(os, "geteuid") and os.geteuid() == 0 else {}
        browser = find_browser()
        if browser:
            cfg["executablePath"] = browser
        cfg_path = os.path.join(work, "puppeteer.json")
        with open(cfg_path, "w") as fh:
            json.dump(cfg, fh)

        outdir = opts.png
        if outdir:
            os.makedirs(outdir, exist_ok=True)
        ext = ".png" if outdir else ".svg"

        def job(item):
            f, line, src = item
            out = os.path.join(outdir or work, slug(f, line) + ext)
            ok, err = render(cmd, cfg_path, src, out, work)
            return item, ok, err, out

        fails = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, opts.jobs)) as pool:
            for (f, line, _), ok, err, out in pool.map(job, work_items):
                where = f"{os.path.relpath(f)}:{line}"
                if ok is None:
                    print(f"UNAVAILABLE {where}\n  {err}")
                    print(
                        "\nmmdc or its headless browser could not run. Say so, and mark each new\n"
                        "diagram with `%% unvalidated` as the first line of its block.\n"
                        "Fixes: `npx puppeteer browsers install chrome-headless-shell`, or set\n"
                        "PUPPETEER_EXECUTABLE_PATH to a local Chrome or Chromium."
                    )
                    pool.shutdown(cancel_futures=True)
                    return 2
                if ok:
                    print(f"PASS {where}" + (f" -> {out}" if outdir else ""))
                else:
                    fails += 1
                    print(f"FAIL {where}")
                    for l in err.splitlines():
                        print(f"  {l}")
        total = len(work_items)
        print(f"\n{total - fails}/{total} Mermaid blocks passed in {len(files)} file(s).")
        return 1 if fails else 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
