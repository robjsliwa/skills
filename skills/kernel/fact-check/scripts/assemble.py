#!/usr/bin/env python3
"""Assemble a page from a template so it cannot disagree with what was verified.

Usage:
  assemble.py TEMPLATE OUT [--values build/values.json] [--claims build/claims.json]
              [--src DIR ...] [--strict-numbers]

Slots in TEMPLATE (HTML or Markdown):
  {{value:NAME}}    a value computed by the values script (values.json), escaped
  {{snip:NAME}}     the lines between `snip:NAME` and `end:NAME` marker lines in
                    any file under the --src folders (the verified code), escaped.
                    A marker line holds only a comment (`// snip:NAME`,
                    `# end:NAME`, `<!-- snip:NAME -->`); other lines are kept verbatim
  {{file:PATH}}     a whole verified file (relative to the first --src), escaped
  {{include:PATH}}  raw HTML inserted as is (a generated figure), relative to TEMPLATE

Slots inside <!-- HTML comments --> are left alone.

Checks, in order; any failure stops the build and writes nothing:
  1. Every slot resolves, and no slot has an unknown kind. (Code that contains
     `{{ }}` itself, like Go or Jinja templates, passes through untouched.)
  2. The claims ledger (if given) has no claim whose status is `pending` or
     `failed`. `unverifiable` claims must carry a `note` and are listed.
  3. Every relative href/src in the output resolves from OUT's folder.
  4. Tags balance (HTML output only).
  5. With --strict-numbers, every number of three or more digits in the prose
     (outside <pre> and <code>) appears in values.json. Without it, such
     numbers are listed as warnings.

Prints counts. Python 3 standard library only.
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path

# A marker is a line holding only a comment: `// snip:name`, `# end:name`,
# `<!-- snip:name -->`, `/* end:name */`, `-- snip:name`, `% end:name`.
MARKER_RE = re.compile(r"^\s*(?:#|//|--|%|;|<!--|/\*)\s*(snip|end):([A-Za-z0-9_.-]+)\s*(?:-->|\*/)?\s*$")
SLOT_RE = re.compile(r"\{\{(value|snip|file|include):([^}\s]+)\}\}")
TAGS = ["p", "div", "section", "figure", "figcaption", "svg", "g", "table", "tr", "td", "th", "pre", "code",
        "details", "summary", "ol", "ul", "li", "aside", "blockquote", "h1", "h2", "h3", "main", "script",
        "text", "span", "a", "strong", "em"]


def find_snippets(src_dirs):
    snips, where = {}, {}
    for d in src_dirs:
        for f in sorted(Path(d).rglob("*")):
            if not f.is_file() or any(part.startswith(".") for part in f.parts):
                continue
            try:
                lines = f.read_text(encoding="utf-8").split("\n")
            except (UnicodeDecodeError, OSError):
                continue
            open_ = {}
            for n, line in enumerate(lines):
                m = MARKER_RE.match(line)
                if not m:
                    continue
                kind, name = m.group(1), m.group(2)
                if kind == "snip":
                    open_[name] = n
                elif name in open_:
                    start = open_.pop(name)
                    body = [l for l in lines[start + 1:n] if not MARKER_RE.match(l)]
                    if name in snips:
                        raise SystemExit(f"snippet '{name}' defined twice: {where[name]} and {f}")
                    snips[name] = "\n".join(body).rstrip("\n")
                    where[name] = str(f)
            for name in open_:
                raise SystemExit(f"snippet '{name}' in {f} has no end:{name}")
    return snips


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("template", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--values", type=Path)
    ap.add_argument("--claims", type=Path)
    ap.add_argument("--src", type=Path, action="append", default=[])
    ap.add_argument("--strict-numbers", action="store_true")
    o = ap.parse_args()

    tpl = o.template.read_text(encoding="utf-8")
    values = json.loads(o.values.read_text(encoding="utf-8")) if o.values else {}
    snips = find_snippets(o.src) if o.src else {}
    errors, warnings, used = [], [], {"value": set(), "snip": set(), "file": set(), "include": set()}

    def fill(m):
        kind, name = m.group(1), m.group(2)
        used[kind].add(name)
        if kind == "value":
            if name not in values:
                errors.append(f"value '{name}' is not in {o.values}")
                return m.group(0)
            v = values[name]
            return html.escape(v if isinstance(v, str) else json.dumps(v), quote=False)
        if kind == "snip":
            if name not in snips:
                errors.append(f"snippet '{name}' not found under {', '.join(map(str, o.src)) or '(no --src)'}")
                return m.group(0)
            return html.escape(snips[name], quote=False)
        if kind == "file":
            if not o.src:
                errors.append(f"{{{{file:{name}}}}} needs --src")
                return m.group(0)
            p = o.src[0] / name
            if not p.exists():
                errors.append(f"file '{p}' does not exist")
                return m.group(0)
            return html.escape(p.read_text(encoding="utf-8").rstrip("\n"), quote=False)
        p = o.template.parent / name
        if not p.exists():
            errors.append(f"include '{p}' does not exist")
            return m.group(0)
        return p.read_text(encoding="utf-8")

    # Slots inside HTML comments are documentation, not slots. Anything shaped
    # like a slot with an unknown kind is a typo; check the template, not the
    # output, so code that itself contains {{ }} (Go, Jinja, Vue) is fine.
    bad = sorted(set(re.findall(r"\{\{(?!(?:value|snip|file|include):)[a-z]+:[^}\s]*\}\}",
                                re.sub(r"<!--.*?-->", "", tpl, flags=re.S))))
    if bad:
        errors.append(f"unknown slot kinds: {bad}")
    parts = re.split(r"(<!--.*?-->)", tpl, flags=re.S)
    out = "".join(p if p.startswith("<!--") else SLOT_RE.sub(fill, p) for p in parts)

    unverifiable = []
    if o.claims:
        claims = json.loads(o.claims.read_text(encoding="utf-8"))
        if not isinstance(claims, list) or not all(isinstance(c, dict) for c in claims):
            errors.append(f"{o.claims} must be a JSON list of claim objects (LEDGER-FORMAT.md)")
            claims = []
        for c in claims:
            st = c.get("status")
            if st in ("pending", "failed", None):
                errors.append(f"claim {c.get('id')}: status {st}: {c.get('text', '')[:80]}")
            elif st == "unverifiable":
                if not c.get("note"):
                    errors.append(f"claim {c.get('id')}: unverifiable with no note saying so to the reader")
                unverifiable.append(c.get("id"))

    is_html = o.out.suffix.lower() in (".html", ".htm")
    for link in set(re.findall(r'(?:href|src)="([^"]+)"', out)):
        if re.match(r"^[a-z][a-z0-9+.-]*:", link, re.I) or link.startswith(("#", "//")):
            continue
        target = (o.out.parent / link.split("#")[0].split("?")[0]).resolve()
        if link.split("#")[0] and not target.exists() and target != o.out.resolve():
            errors.append(f"link does not resolve from {o.out.parent}: {link}")

    if is_html:
        body = re.sub(r"<!--.*?-->", "", out, flags=re.S)
        body = re.sub(r"<script\b.*?</script>", "<script></script>", body, flags=re.S)
        for tag in TAGS:
            opens = len(re.findall(rf"<{tag}[\s>]", body))
            closes = len(re.findall(rf"</{tag}>", body))
            if opens != closes:
                errors.append(f"<{tag}> opens {opens} times, closes {closes}")

    prose = re.sub(r"<(pre|code|script|style)\b.*?</\1>", " ", out, flags=re.S)
    prose = re.sub(r"```.*?```|`[^`]*`", " ", prose, flags=re.S)
    prose = re.sub(r"<[^>]+>", " ", prose)
    num_re = r"(?<![\w.#-])\d[\d,.]*\d(?![\w-])"
    norm = lambda n: n.replace(",", "").rstrip(".")
    known = {norm(t) for v in values.values()
             for t in re.findall(num_re, v if isinstance(v, str) else json.dumps(v))}
    stray = sorted({n for n in re.findall(num_re, prose)
                    if len(re.sub(r"\D", "", n)) >= 3 and norm(n) not in known})
    if stray:
        (errors if o.strict_numbers else warnings).append(
            "numbers in prose not produced by the values script: " + ", ".join(stray[:30]))

    for w in warnings:
        print(f"  WARN  {w}")
    if errors:
        for e in errors:
            print(f"  FAIL  {e}")
        print(f"Not written: {len(errors)} problem(s).")
        return 1
    o.out.parent.mkdir(parents=True, exist_ok=True)
    o.out.write_text(out, encoding="utf-8")
    print(f"wrote {o.out} ({len(out):,} bytes): {len(used['value'])} values, {len(used['snip'])} snippets, "
          f"{len(used['file'])} files, {len(used['include'])} includes"
          + (f"; unverifiable claims flagged to the reader: {', '.join(unverifiable)}" if unverifiable else ""))
    unused = sorted(set(values) - used["value"])
    if unused:
        print(f"  note  values computed but not quoted: {', '.join(unused[:20])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
