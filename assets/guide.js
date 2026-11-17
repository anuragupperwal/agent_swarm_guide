/* Loop to Swarm: theme toggle, auto table of contents, "I can explain this" progress.
   Loaded in <head> without defer so the saved theme applies before first paint.
   All storage access is wrapped: the guide must work with storage blocked. */
(function () {
  var THEME_KEY = "l2s-theme";
  var DONE_KEY = "l2s-done";
  var root = document.documentElement;

  function read(key) {
    try { return window.localStorage.getItem(key); } catch (e) { return null; }
  }
  function write(key, value) {
    try { window.localStorage.setItem(key, value); } catch (e) { /* storage unavailable */ }
  }
  function doneList() {
    try {
      var v = JSON.parse(read(DONE_KEY) || "[]");
      return Array.isArray(v) ? v : [];
    } catch (e) { return []; }
  }

  var saved = read(THEME_KEY);
  if (saved === "light" || saved === "dark") root.setAttribute("data-theme", saved);

  function effectiveTheme() {
    var t = root.getAttribute("data-theme");
    if (t === "light" || t === "dark") return t;
    try {
      return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    } catch (e) { return "light"; }
  }

  document.addEventListener("DOMContentLoaded", function () {
    /* Theme toggle */
    var btn = document.getElementById("theme-toggle");
    function label() {
      if (btn) btn.textContent = effectiveTheme() === "dark" ? "Light theme" : "Dark theme";
    }
    if (btn) {
      label();
      btn.addEventListener("click", function () {
        var next = effectiveTheme() === "dark" ? "light" : "dark";
        root.setAttribute("data-theme", next);
        write(THEME_KEY, next);
        label();
      });
    }

    /* Auto table of contents from h2[id] inside main.chapter */
    var main = document.querySelector("main.chapter");
    var targets = document.querySelectorAll("[data-toc]");
    if (main && targets.length) {
      var heads = main.querySelectorAll("h2[id]");
      Array.prototype.forEach.call(targets, function (target) {
        var ol = document.createElement("ol");
        Array.prototype.forEach.call(heads, function (h) {
          var li = document.createElement("li");
          var a = document.createElement("a");
          a.href = "#" + h.id;
          a.textContent = h.getAttribute("data-short") || h.textContent;
          li.appendChild(a);
          ol.appendChild(li);
        });
        target.appendChild(ol);
      });
    }

    /* Chapter "I can explain this" checkbox */
    var toggle = document.getElementById("done-toggle");
    if (toggle) {
      var ch = toggle.getAttribute("data-chapter");
      toggle.checked = doneList().indexOf(ch) !== -1;
      toggle.addEventListener("change", function () {
        var list = doneList().filter(function (x) { return x !== ch; });
        if (toggle.checked) list.push(ch);
        write(DONE_KEY, JSON.stringify(list));
      });
    }

    /* Home page progress */
    var rows = document.querySelectorAll("[data-ch]");
    if (rows.length) {
      var done = doneList();
      var count = 0;
      Array.prototype.forEach.call(rows, function (r) {
        if (done.indexOf(r.getAttribute("data-ch")) !== -1) {
          r.classList.add("is-done");
          count++;
        }
      });
      var out = document.getElementById("progress-count");
      if (out) out.textContent = String(count);
    }
  });
})();
