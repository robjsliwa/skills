// Shared SVG <defs> for .fig illustrations: four arrowheads and the "sketch"
// wobble filter that gives straight lines a hand-drawn look. Include once per
// page, after the figures:  <script src="../assets/figures.js"></script>
(function () {
  function marker(id, color) {
    return '<marker id="' + id + '" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">' +
      '<path d="M1 1 L9 5 L1 9" fill="none" stroke="' + color + '" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>';
  }
  var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("aria-hidden", "true");
  svg.setAttribute("style", "position:absolute;width:0;height:0;overflow:hidden");
  svg.innerHTML = "<defs>" +
    marker("arr", "#1a1a1a") + marker("arr-acc", "#8b2500") + marker("arr-ok", "#1d6b3a") + marker("arr-bad", "#a52a1d") +
    '<filter id="sketch" x="-5%" y="-5%" width="110%" height="110%">' +
    '<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7" result="n"/>' +
    '<feDisplacementMap in="SourceGraphic" in2="n" scale="1.6" xChannelSelector="R" yChannelSelector="G"/>' +
    "</filter></defs>";
  document.body.insertBefore(svg, document.body.firstChild);
})();
