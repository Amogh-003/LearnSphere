document.addEventListener("DOMContentLoaded", function () {
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = "opacity 0.5s";
      alert.style.opacity = "0";
      setTimeout(function () { alert.remove(); }, 500);
    }, 4000);
  });

  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      document.body.classList.toggle("light-theme");
      localStorage.setItem(
        "learnsphere-theme",
        document.body.classList.contains("light-theme") ? "light" : "dark"
      );
    });
  }

  if (localStorage.getItem("learnsphere-theme") === "light") {
    document.body.classList.add("light-theme");
  }
});
