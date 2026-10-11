/* GEM website · site behaviour · v0.4
   Progressive enhancement: the page works without this file. Each feature is installed in its
   own guarded block and only switches its UI on after its handlers are in place.
   - Navigation disclosure (compact to tablet widths)       — audit GEM-02
   - Enquiry form: fail-closed preparation (no native submit) — GEM-01
     stale-draft invalidation                                — GEM-04
   - Header: stays reachable on long pages (hides while reading down, returns on scroll up)
   - Section links: "you are here" marking in the navigation (aria-current="location")
   - Section calls to action preselect the enquiry topic
   - Delivery: no webpage submission. Owner-approved email-app handoff only; see DELIVERY.
   No network request is made by this file. */
(function () {
  "use strict";

  /* Owner-supplied enquiry address (WD-12). Both the enquiry form and the quotation request
     hand their draft to the visitor's email app; this page itself sends nothing. */
  var MAILTO = "mish3labdul@gmail.com";
  var mailtoOk = function (a) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(a) && !/\.(example|invalid|test)$/i.test(a); };

  /* ---------- Navigation disclosure ---------- */
  try {
    var header = document.querySelector(".site-header");
    var toggle = header && header.querySelector(".nav-toggle");
    var nav = document.getElementById("primary-nav");
    if (header && toggle && nav) {
      var setOpen = function (open) {
        header.classList.toggle("is-open", open);
        toggle.setAttribute("aria-expanded", String(open));
        toggle.textContent = open ? "Close" : "Menu";
      };
      toggle.addEventListener("click", function () { setOpen(toggle.getAttribute("aria-expanded") !== "true"); });
      nav.addEventListener("click", function (e) { if (e.target.closest("a")) setOpen(false); });
      /* Close when the visitor taps outside the menu (including the scrim) or tabs out of it. */
      document.addEventListener("click", function (e) {
        if (toggle.getAttribute("aria-expanded") === "true" && !nav.contains(e.target) && !toggle.contains(e.target)) setOpen(false);
      });
      header.addEventListener("focusout", function (e) {
        if (toggle.getAttribute("aria-expanded") === "true" && e.relatedTarget && !header.contains(e.relatedTarget)) setOpen(false);
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") { setOpen(false); toggle.focus(); }
      });
      var mq = window.matchMedia("(min-width: 1024px)");
      var onMq = function () { if (mq.matches) setOpen(false); };
      if (mq.addEventListener) mq.addEventListener("change", onMq); else if (mq.addListener) mq.addListener(onMq);
      /* Handlers are installed: only now collapse the list behind the button. */
      toggle.hidden = false;
      header.classList.add("nav-ready");
    }
  } catch (err) {
    /* Leave the always-visible navigation in place. */
  }

  /* ---------- Header that stays reachable (audit C2) ----------
     CSS makes the header sticky only where the viewport is tall enough (see site.css). Here it
     steps out of the way while the visitor reads down and comes back as soon as they scroll up.
     Opacity only, per the motion rules; reduced motion makes it instant. */
  try {
    var hdr = document.querySelector(".site-header");
    if (hdr && window.matchMedia) {
      var tall = window.matchMedia("(min-height: 560px)");
      var root = document.documentElement;
      var setH = function () { root.style.setProperty("--header-h", (tall.matches ? hdr.offsetHeight : 0) + "px"); };
      setH();
      window.addEventListener("resize", setH);
      var lastY = window.scrollY, ticking = false;
      var update = function () {
        ticking = false;
        var y = window.scrollY;
        var keep = !tall.matches || y < hdr.offsetHeight || hdr.classList.contains("is-open") || hdr.contains(document.activeElement);
        if (keep || y < lastY - 4) hdr.classList.remove("is-tucked");
        else if (y > lastY + 4) hdr.classList.add("is-tucked");
        lastY = y;
      };
      window.addEventListener("scroll", function () { if (!ticking) { ticking = true; window.requestAnimationFrame(update); } }, { passive: true });
      hdr.addEventListener("focusin", function () { hdr.classList.remove("is-tucked"); });
    }
  } catch (err) { /* the header simply stays in place */ }

  /* ---------- "You are here" in section navigation (audit I5) ---------- */
  try {
    if ("IntersectionObserver" in window) {
      var groups = [document.querySelectorAll('#primary-nav a[href^="#"]'), document.querySelectorAll('.ref-toc a[href^="#"]')];
      groups.forEach(function (links) {
        if (!links.length) return;
        var byId = {};
        Array.prototype.forEach.call(links, function (a) { var t = document.getElementById(a.getAttribute("href").slice(1)); if (t) byId[t.id] = a; });
        var mark = function (id) {
          Array.prototype.forEach.call(links, function (a) { a.removeAttribute("aria-current"); });
          if (id && byId[id]) byId[id].setAttribute("aria-current", "location");
        };
        var visible = {};
        var io = new IntersectionObserver(function (entries) {
          entries.forEach(function (en) { visible[en.target.id] = en.isIntersecting; });
          var current = null;
          Object.keys(byId).forEach(function (id) { if (visible[id] && !current) current = id; });
          mark(current);
        }, { rootMargin: "-35% 0px -60% 0px" });
        Object.keys(byId).forEach(function (id) { io.observe(document.getElementById(id)); });
      });
    }
  } catch (err) { /* navigation still works without the marker */ }

  /* ---------- Section calls to action choose the enquiry topic (audit C2) ---------- */
  try {
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a[data-interest]");
      if (!a) return;
      var radio = document.getElementById(a.getAttribute("data-interest"));
      if (radio && !radio.checked) {
        radio.checked = true;
        /* Fire change so an existing draft is withdrawn (GEM-04). */
        radio.dispatchEvent(new Event("change", { bubbles: true }));
      }
    });
  } catch (err) { /* the link still goes to the form */ }

  /* ---------- Quotation request: Ready packages (2026-10-11) ----------
     Same fail-closed pattern as the enquiry form: submit is prevented first and the button is
     enabled only after every handler is installed. No prices or quantities are invented; the
     request carries only what the visitor chose. */
  var qf = document.getElementById("quote-form");
  if (qf) {
    qf.addEventListener("submit", function (e) { e.preventDefault(); });
    try {
      var q$ = function (id) { return document.getElementById(id); };
      var qButton = q$("quote-button"), qSummary = q$("quote-error-summary"), qList = q$("quote-error-list");
      var qResult = q$("quote-result"), qOut = q$("q-output"), qEmail = q$("quote-email"), qCopy = q$("quote-copy");
      var qCopyStatus = q$("quote-copy-status"), qStatus = q$("quote-status"), qRooms = q$("q-rooms");
      var qSampling = q$("q-sampling"), qSamplingStatus = q$("q-sampling-status"), qStationery = q$("q-stationery");
      var qDraft = false;
      var qRules = [
        { id: "q-package", first: "pkg-room", msg: "Choose a package.", ok: function () { return !!qf.querySelector('input[name="package"]:checked'); } },
        { id: "q-rooms", first: "q-rooms", msg: "Enter a whole number of rooms from 1 to 100,000.", ok: function () { var v = qRooms.value.trim(); return /^[0-9]+$/.test(v) && +v >= 1 && +v <= 100000; } }
      ];
      var qSetError = function (rule, msg) {
        var err = q$(rule.id + "-error");
        err.textContent = msg || ""; err.hidden = !msg;
        if (rule.id === "q-rooms") {
          if (msg) { qRooms.setAttribute("aria-invalid", "true"); qRooms.setAttribute("aria-describedby", "q-rooms-hint q-rooms-error"); }
          else { qRooms.removeAttribute("aria-invalid"); qRooms.setAttribute("aria-describedby", "q-rooms-hint"); }
        } else {
          Array.prototype.forEach.call(qf.querySelectorAll('input[name="package"]'), function (r) { if (msg) r.setAttribute("aria-invalid", "true"); else r.removeAttribute("aria-invalid"); });
        }
      };
      var qClear = function () {
        qResult.hidden = true; qOut.value = ""; qCopyStatus.textContent = "";
        qEmail.hidden = true; qEmail.removeAttribute("href"); qDraft = false;
      };
      var qEdited = function () {
        if (qDraft) { qClear(); qStatus.textContent = "Your choices changed. Request the quotation again to update it."; }
      };
      qf.addEventListener("input", function (e) { if (e.target !== qOut) qEdited(); });
      qf.addEventListener("change", function (e) { if (e.target !== qOut) qEdited(); });

      /* Part B ToggleButton: label, pressed state and a status sentence all change. */
      qSampling.addEventListener("click", function () {
        var on = qSampling.getAttribute("aria-pressed") !== "true";
        qSampling.setAttribute("aria-pressed", String(on));
        qSampling.textContent = on ? "Remove sampling from brief" : "Add sampling to brief";
        qSamplingStatus.textContent = on ? "Sampling selected." : "Sampling not selected.";
        qEdited();
      });

      qf.addEventListener("submit", function () {
        qClear(); qStatus.textContent = "";
        var errors = [];
        qRules.forEach(function (r) { var ok = r.ok(); qSetError(r, ok ? "" : r.msg); if (!ok) errors.push(r); });
        if (errors.length) {
          qList.innerHTML = "";
          errors.forEach(function (r) {
            var li = document.createElement("li"), a = document.createElement("a");
            a.href = "#" + r.first; a.textContent = r.msg;
            a.addEventListener("click", function (ev) { ev.preventDefault(); q$(r.first).focus(); });
            li.appendChild(a); qList.appendChild(li);
          });
          qSummary.hidden = false;
          q$(errors[0].first).focus();
          return;
        }
        qSummary.hidden = true;
        var pkg = qf.querySelector('input[name="package"]:checked').value;
        qOut.value = [
          "Quotation request for GEM",
          "Package: " + pkg,
          "Rooms to supply: " + qRooms.value.trim(),
          "Arrival stationery: " + (qStationery.checked ? "Yes" : "No"),
          "Sampling: " + (qSampling.getAttribute("aria-pressed") === "true" ? "Yes" : "No")
        ].join("\n");
        if (mailtoOk(MAILTO)) {
          qEmail.setAttribute("href", "mailto:" + MAILTO + "?subject=" + encodeURIComponent("Quotation request for GEM: " + pkg) + "&body=" + encodeURIComponent(qOut.value));
          qEmail.hidden = false;
        }
        qDraft = true; qResult.hidden = false; qResult.focus();
      });

      qCopy.addEventListener("click", function () {
        if (!qDraft) return;
        var done = function () { qCopyStatus.textContent = "Copied to your clipboard."; };
        var fail = function () { qOut.focus(); qOut.select(); qCopyStatus.textContent = "Copy is not available here. The text is selected; copy it with your keyboard."; };
        try { if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(qOut.value).then(done, fail); else fail(); } catch (err) { fail(); }
      });

      q$("quote-unavailable").hidden = true;
      /* The unavailable notice is now hidden: stop describing the button with it (Part B Field). */
      qButton.setAttribute("aria-describedby", "quote-intro");
      qButton.disabled = false;
    } catch (err) {
      /* The button stays disabled and the notice stays visible. */
    }
  }

  /* ---------- Enquiry form ---------- */
  var form = document.getElementById("enquiry-form");
  if (!form) return;

  /* Installed first and unconditionally: no path through this script submits natively. */
  form.addEventListener("submit", function (e) { e.preventDefault(); });

  try {
    /* DELIVERY — switched off. To connect a destination later (separate authorization required):
       set endpoint to an HTTPS URL that accepts JSON and returns 2xx on success. Until then the
       form only prepares a local draft and says so. */
    var DELIVERY = { endpoint: "" };
    /* Interim hand-off (audit C1): when GEM supplies a real, monitored address, put it here and
       the drafted enquiry gains an "Open in your email app" button. Empty = hidden. Never use a
       placeholder or third-party address. */
    DELIVERY.mailto = MAILTO;

    var $ = function (id) { return document.getElementById(id); };
    var prepareButton = $("prepare-button");
    var unavailable = $("form-unavailable");
    var summary = $("error-summary");
    var list = $("error-list");
    var result = $("form-result");
    var output = $("f-output");
    var copyBtn = $("copy-output");
    var copyStatus = $("copy-status");
    var emailOut = $("email-output");
    var draftStatus = $("draft-status");
    var trap = $("f-website");
    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var hasDraft = false;

    var rules = [
      { id: "f-name", test: function (v) { return v.trim() !== ""; }, msg: "Enter your name." },
      { id: "f-email", test: function (v) { return emailPattern.test(v.trim()); }, msg: "Enter an email address in the format name@example.com." },
      { id: "f-interest", radio: "interest", msg: "Choose what your enquiry is about." },
      { id: "f-message", test: function (v) { return v.trim() !== ""; }, msg: "Tell us a little about your property or project." }
    ];
    var controlsFor = function (rule) {
      return rule.radio ? Array.prototype.slice.call(form.querySelectorAll('input[name="' + rule.radio + '"]')) : [$(rule.id)];
    };

    var setFieldError = function (rule, message) {
      var err = $(rule.id + "-error");
      controlsFor(rule).forEach(function (c) {
        /* Keep any help text in the description and add the error after it (Part B Field). */
        if (!c.hasAttribute("data-describedby")) c.setAttribute("data-describedby", c.getAttribute("aria-describedby") || "");
        var base = c.getAttribute("data-describedby");
        if (message) {
          c.setAttribute("aria-invalid", "true");
          if (!rule.radio) c.setAttribute("aria-describedby", (base ? base + " " : "") + rule.id + "-error");
        } else {
          c.removeAttribute("aria-invalid");
          if (!rule.radio) { if (base) c.setAttribute("aria-describedby", base); else c.removeAttribute("aria-describedby"); }
        }
      });
      err.textContent = message || "";
      err.hidden = !message;
    };

    var validate = function () {
      var errors = [];
      rules.forEach(function (rule) {
        var ok = rule.radio ? !!form.querySelector('input[name="' + rule.radio + '"]:checked') : rule.test($(rule.id).value);
        setFieldError(rule, ok ? "" : rule.msg);
        if (!ok) errors.push(rule);
      });
      return errors;
    };

    var value = function (name) { var el = form.elements[name]; return el ? String(el.value || "").trim() : ""; };
    var compose = function () {
      var interest = form.querySelector('input[name="interest"]:checked');
      return [
        "Enquiry for GEM",
        "Name: " + value("name"),
        "Email: " + value("email"),
        "Organisation or property: " + (value("organisation") || "Not given"),
        "About: " + (interest ? interest.value : ""),
        "",
        value("message")
      ].join("\n");
    };

    var clearDraft = function () {
      result.hidden = true;
      output.value = "";
      copyStatus.textContent = "";
      if (emailOut) { emailOut.hidden = true; emailOut.removeAttribute("href"); }
      hasDraft = false;
    };

    /* GEM-04: any edit after preparing withdraws the draft, so a stale copy cannot be taken. */
    var onEdit = function (e) {
      if (e.target === trap || e.target === output) return;
      if (hasDraft) {
        clearDraft();
        draftStatus.textContent = "Your details changed. Draft the enquiry again to update it.";
      }
    };
    form.addEventListener("input", onEdit);
    form.addEventListener("change", onEdit);

    form.addEventListener("submit", function () {
      clearDraft();
      draftStatus.textContent = "";
      var errors = validate();
      if (errors.length) {
        list.innerHTML = "";
        errors.forEach(function (rule) {
          var target = controlsFor(rule)[0];
          var li = document.createElement("li");
          var a = document.createElement("a");
          a.href = "#" + target.id;
          a.textContent = rule.msg;
          a.addEventListener("click", function (ev) { ev.preventDefault(); target.focus(); });
          li.appendChild(a);
          list.appendChild(li);
        });
        summary.hidden = false;
        controlsFor(errors[0])[0].focus();
        return;
      }
      summary.hidden = true;
      if (trap && trap.value) return; /* automated fill: do nothing */
      /* DELIVERY.endpoint is empty, so nothing is sent. */
      output.value = compose();
      if (emailOut && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(DELIVERY.mailto) && !/\.(example|invalid|test)$/i.test(DELIVERY.mailto)) {
        emailOut.setAttribute("href", "mailto:" + DELIVERY.mailto + "?subject=" + encodeURIComponent("Enquiry for GEM") + "&body=" + encodeURIComponent(output.value));
        emailOut.hidden = false;
      }
      hasDraft = true;
      result.hidden = false;
      result.focus();
    });

    form.addEventListener("reset", function () {
      rules.forEach(function (rule) { setFieldError(rule, ""); });
      summary.hidden = true;
      clearDraft();
      draftStatus.textContent = "";
      setTimeout(function () { $("f-name").focus(); }, 0);
    });

    copyBtn.addEventListener("click", function () {
      if (!hasDraft) return;
      var done = function () { copyStatus.textContent = "Copied to your clipboard."; };
      var fail = function () { output.focus(); output.select(); copyStatus.textContent = "Copy is not available here. The text is selected; copy it with your keyboard."; };
      try {
        if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(output.value).then(done, fail);
        else fail();
      } catch (err) { fail(); }
    });

    if (DELIVERY.endpoint) { /* reserved for an authorized connection; intentionally unused */ }

    /* Everything is installed: switch the form on. */
    unavailable.hidden = true;
    /* The unavailable notice is now hidden: stop describing the button with it (Part B Field). */
    prepareButton.setAttribute("aria-describedby", "form-intro");
    prepareButton.disabled = false;
  } catch (err) {
    /* Initialization failed: the button stays disabled and the unavailable notice stays visible. */
  }
})();
