// Game Guru concept mockup: small progressive enhancements. Every page is readable without this file.
(function () {
  "use strict";

  function store(key, value) {
    try {
      if (value === undefined) return localStorage.getItem(key);
      localStorage.setItem(key, value);
    } catch (e) { return null; }
  }

  // Mobile menu
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Venue switcher: shows venue-specific content and remembers the choice
  var venueSelect = document.getElementById("venue");
  function applyVenue(v) {
    document.querySelectorAll("[data-venue]").forEach(function (el) {
      var list = el.getAttribute("data-venue").split(" ");
      el.hidden = list.indexOf(v) === -1 && list.indexOf("all") === -1;
    });
    document.querySelectorAll("[data-venue-name]").forEach(function (el) {
      el.textContent = v === "touchwood" ? "Touchwood, Solihull" : "Utilita Arena, Birmingham";
    });
    var bookVenue = document.getElementById("b-venue");
    if (bookVenue) bookVenue.value = v;
  }
  if (venueSelect) {
    var saved = store("gg-venue");
    if (saved) venueSelect.value = saved;
    applyVenue(venueSelect.value);
    venueSelect.addEventListener("change", function () {
      store("gg-venue", venueSelect.value);
      applyVenue(venueSelect.value);
    });
  }

  // Booking drawer
  var drawer = document.getElementById("book-drawer");
  document.querySelectorAll("[data-book]").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      if (!drawer || typeof drawer.showModal !== "function") return; // falls back to the #book link
      e.preventDefault();
      var type = btn.getAttribute("data-book");
      var sel = document.getElementById("b-type");
      if (sel && type) sel.value = type;
      drawer.showModal();
    });
  });
  document.querySelectorAll("[data-close]").forEach(function (btn) {
    btn.addEventListener("click", function () { drawer && drawer.close(); });
  });

  // Mock forms: never submit anywhere, show a confirmation instead
  document.querySelectorAll("form[data-mock]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var out = form.querySelector(".confirm");
      if (out) {
        out.hidden = false;
        out.textContent = form.getAttribute("data-mock");
        out.focus && out.focus();
      }
    });
  });

  // Tabs
  document.querySelectorAll("[role=tablist]").forEach(function (list) {
    var tabs = list.querySelectorAll("[role=tab]");
    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        tabs.forEach(function (t) {
          var on = t === tab;
          t.setAttribute("aria-selected", on ? "true" : "false");
          var panel = document.getElementById(t.getAttribute("aria-controls"));
          if (panel) panel.hidden = !on;
        });
      });
    });
  });

  // Filter chips: each group filters items by a data attribute
  document.querySelectorAll("[data-filter-target]").forEach(function (root) {
    var items = document.querySelectorAll(root.getAttribute("data-filter-target"));
    var count = document.querySelector(root.getAttribute("data-filter-count") || "#none");
    function run() {
      var active = {};
      root.querySelectorAll(".chip[aria-pressed=true]").forEach(function (c) {
        var k = c.getAttribute("data-key");
        (active[k] = active[k] || []).push(c.getAttribute("data-val"));
      });
      var shown = 0;
      items.forEach(function (item) {
        var ok = Object.keys(active).every(function (k) {
          var have = (item.getAttribute("data-" + k) || "").split(" ");
          return active[k].some(function (v) { return have.indexOf(v) !== -1; });
        });
        item.hidden = !ok;
        if (ok) shown++;
      });
      if (count) count.textContent = shown;
    }
    root.querySelectorAll(".chip").forEach(function (c) {
      c.addEventListener("click", function () {
        c.setAttribute("aria-pressed", c.getAttribute("aria-pressed") === "true" ? "false" : "true");
        run();
      });
    });
    run();
  });

  // Singles search
  var singlesSearch = document.getElementById("singles-search");
  if (singlesSearch) {
    singlesSearch.addEventListener("input", function () {
      var q = singlesSearch.value.trim().toLowerCase();
      document.querySelectorAll("#singles-body tr").forEach(function (row) {
        row.hidden = q && row.textContent.toLowerCase().indexOf(q) === -1;
      });
    });
  }

  // Lore counter (first to 20 wins)
  document.querySelectorAll("[data-lore]").forEach(function (root) {
    var scores = [0, 0];
    var win = root.querySelector(".win");
    function draw() {
      [0, 1].forEach(function (i) {
        root.querySelector("[data-score='" + i + "']").textContent = scores[i];
        root.querySelector("[data-bar='" + i + "']").style.width = Math.min(scores[i], 20) * 5 + "%";
      });
      var w = scores.indexOf(Math.max.apply(null, scores));
      win.textContent = scores[w] >= 20 ? (w === 0 ? "Player 1" : "Player 2") + " reaches 20 lore and wins" : "";
    }
    root.querySelectorAll("[data-p]").forEach(function (b) {
      b.addEventListener("click", function () {
        var p = +b.getAttribute("data-p");
        scores[p] = Math.max(0, scores[p] + (+b.getAttribute("data-d")));
        draw();
      });
    });
    var reset = root.querySelector("[data-reset]");
    if (reset) reset.addEventListener("click", function () { scores = [0, 0]; draw(); });
    draw();
  });

  // Two-player chess clock
  document.querySelectorAll("[data-clock]").forEach(function (root) {
    var start = 10 * 60;
    var t = [start, start], active = -1, timer = null;
    var faces = root.querySelectorAll("button.face");
    function fmt(s) { var m = Math.floor(s / 60), r = s % 60; return m + ":" + (r < 10 ? "0" : "") + r; }
    function draw() {
      faces.forEach(function (f, i) {
        f.querySelector("b").textContent = fmt(t[i]);
        f.classList.toggle("active", i === active);
        f.setAttribute("aria-pressed", i === active ? "true" : "false");
      });
    }
    function tick() {
      if (active < 0) return;
      t[active] = Math.max(0, t[active] - 1);
      if (t[active] === 0) { clearInterval(timer); timer = null; }
      draw();
    }
    faces.forEach(function (f, i) {
      f.addEventListener("click", function () {
        active = i === 0 ? 1 : 0; // tapping your clock ends your turn
        if (!timer) timer = setInterval(tick, 1000);
        draw();
      });
    });
    root.querySelector("[data-pause]").addEventListener("click", function () { clearInterval(timer); timer = null; active = -1; draw(); });
    root.querySelector("[data-reset]").addEventListener("click", function () { clearInterval(timer); timer = null; active = -1; t = [start, start]; draw(); });
    draw();
  });

  // Cyberpunk RED style tracker
  document.querySelectorAll("[data-tracker]").forEach(function (root) {
    var maxHp = 40;
    var vals = { hp: 40, hum: 50, ammo: 8 };
    function draw() {
      Object.keys(vals).forEach(function (k) { root.querySelector("[data-out='" + k + "']").textContent = vals[k]; });
      var bar = root.querySelector("[data-hpbar]");
      bar.style.width = (vals.hp / maxHp) * 100 + "%";
      bar.classList.toggle("low", vals.hp <= maxHp / 2);
      var state = root.querySelector("[data-state]");
      state.textContent = vals.hp <= 0 ? "Mortally wounded" : vals.hp <= maxHp / 2 ? "Seriously wounded" : "";
    }
    root.querySelectorAll("[data-k]").forEach(function (b) {
      b.addEventListener("click", function () {
        var k = b.getAttribute("data-k");
        vals[k] = Math.max(0, vals[k] + (+b.getAttribute("data-d")));
        if (k === "hp") vals.hp = Math.min(maxHp, vals.hp);
        draw();
      });
    });
    draw();
  });
})();
