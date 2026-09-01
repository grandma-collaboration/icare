document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".md-nav__link[href^='http']").forEach(function (link) {
    link.setAttribute("target", "_blank");
    link.setAttribute("rel", "noopener");
  });
});
