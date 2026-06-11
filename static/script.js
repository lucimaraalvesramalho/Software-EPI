const button = document.getElementById("theme-btn");
const icon = document.getElementById("theme-icon");

const setTheme = (dark) => {
    document.body.classList.toggle("dark-theme", dark);
    icon.classList.toggle("fa-sun", dark);
    icon.classList.toggle("fa-moon", !dark);
    localStorage.setItem("theme", dark ? "dark" : "light");
};

setTheme(localStorage.getItem("theme") === "dark");

button.addEventListener("click", () => {
    setTheme(!document.body.classList.contains("dark-theme"));
});
