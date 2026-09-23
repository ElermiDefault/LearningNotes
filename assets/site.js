(function () {
  const root = document.documentElement;
  const button = document.querySelector("[data-theme-toggle]");
  const saved = localStorage.getItem("study-log-theme");
  const preferredDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

  function applyTheme(theme) {
    root.dataset.theme = theme;
    if (button) {
      button.textContent = theme === "dark" ? "浅色" : "深色";
      button.setAttribute("aria-label", theme === "dark" ? "切换到浅色主题" : "切换到深色主题");
    }
  }

  applyTheme(saved || (preferredDark ? "dark" : "light"));

  if (button) {
    button.addEventListener("click", function () {
      const next = root.dataset.theme === "dark" ? "light" : "dark";
      localStorage.setItem("study-log-theme", next);
      applyTheme(next);
    });
  }
})();
