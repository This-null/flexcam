let S = {};
let CFG = {};
let updateUrl = null;
let remoteOn = false;
let quality = "medium";
let theme = "default";
let running = false;
let lastState = null;
let lastInfo = null;

function $(id) { return document.getElementById(id); }

function applyStrings() {
  $("tagline").textContent = S.tagline;
  $("statusText").textContent = S.status_ready;
  $("wifiLabel").textContent = S.wifi_label;
  $("wifiIp").placeholder = "192.168.1.x";
  $("toggleBtn").textContent = S.btn_start;
  $("installLabel").textContent = S.btn_install;
  $("trayLabel").textContent = S.setting_tray;
  $("usbLabel").textContent = S.usb_label;
  $("privacy").textContent = "🔒 " + S.privacy_note;
  $("statusCaption").textContent = S.status_caption;
  $("setAppearanceTitle").textContent = S.setting_appearance;
  $("setMotionTitle").textContent = S.setting_motion;
  $("motionHelp").textContent = S.setting_motion_help;
  $("motionSystem").textContent = S.motion_system;
  $("motionFull").textContent = S.motion_full;
  $("motionReduced").textContent = S.motion_reduced;
  $("setGeneralTitle").textContent = S.setting_general;
  $("navHomeLabel").textContent = S.nav_home;
  $("navEffectsLabel").textContent = S.nav_effects;
  $("effectsTitle").textContent = S.effects_title;
  $("fxPresetsTitle").textContent = S.effects_presets;
  $("fxAdjustTitle").textContent = S.effects_adjust;
  document.querySelectorAll(".preset-card").forEach((c) => {
    c.querySelector(".name").textContent = S["fx_" + c.dataset.preset];
  });
  document.querySelectorAll("[data-fxlabel]").forEach((e) => {
    e.textContent = S["fx_" + e.dataset.fxlabel];
  });
  $("fxMirrorTitle").textContent = S.fx_mirror;
  $("fxMirrorHelp").textContent = S.fx_mirror_help;
  $("fxResetLabel").textContent = S.fx_reset;
  $("fxNote").textContent = S.fx_note;
  $("settingsLabel").textContent = S.settings;
  $("settingsTitle").textContent = S.settings;
  $("setThemeTitle").textContent = S.setting_theme;
  $("setLangTitle").textContent = S.setting_language;
  $("discordTitle").textContent = S.setting_discord;
  $("discordHelp").textContent = S.setting_discord_help;
  $("remoteLabel").textContent = S.remote_label || "Remote";
  $("remoteExp").textContent = S.remote_experimental || "Experimental";
  $("remoteHelp").textContent = S.remote_help || "";
  $("remoteBtn").textContent = remoteOn
    ? (S.remote_stop || "Stop remote")
    : (S.remote_start || "Start remote");
  $("qLowName").textContent = S.q_low || "Low";
  $("qMedName").textContent = S.q_medium || "Medium";
  $("qHighName").textContent = S.q_high || "High";
  $("qLowSub").textContent = S.q_low_sub || "";
  $("qMedSub").textContent = S.q_medium_sub || "";
  $("qHighSub").textContent = S.q_high_sub || "";
}

let fadeTimer = null;

function applyTheme(name) {
  const root = document.documentElement;
  root.classList.add("theme-fade");
  clearTimeout(fadeTimer);
  fadeTimer = setTimeout(() => root.classList.remove("theme-fade"), 420);
  theme = name || "default";
  if (theme === "default") document.documentElement.removeAttribute("data-theme");
  else document.documentElement.setAttribute("data-theme", theme);
  document.querySelectorAll(".theme-card").forEach((d) => {
    const on = d.dataset.theme === theme;
    d.classList.toggle("active", on);
    d.setAttribute("aria-pressed", on);
  });
}

function isReduced() {
  const m = document.documentElement.dataset.motion;
  return m === "reduced" || (m !== "full" && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
}

function applyMotion(mode) {
  document.documentElement.dataset.motion = mode;
  document.querySelectorAll("#motionSeg button").forEach((b) => {
    b.setAttribute("aria-pressed", b.dataset.motion === mode);
  });
}

function runIntro() {
  const el = $("intro");
  if (!el) return;
  if (isReduced()) { el.remove(); return; }
  setTimeout(() => {
    el.classList.add("out");
    setTimeout(() => el.remove(), 320);
  }, 1100);
}

const PAGES = { home: "mainView", effects: "cameraView", settings: "settingsView" };
let currentPage = "home";
let previewUrl = "";

function showPage(name) {
  currentPage = name;
  for (const [k, id] of Object.entries(PAGES)) $(id).classList.toggle("hidden", k !== name);
  document.querySelectorAll(".page-item").forEach((b) => {
    const on = b.dataset.page === name;
    b.classList.toggle("active", on);
    if (on) b.setAttribute("aria-current", "page"); else b.removeAttribute("aria-current");
  });
  if (name === "effects" && previewUrl) $("fxPreview").src = previewUrl;
  else $("fxPreview").removeAttribute("src");
}

const FX_KEYS = ["brightness", "contrast", "saturation", "warmth", "shadows", "sharpness"];
let fx = { params: {}, preset: "original", presets: {} };
let fxTimer = null;

function renderFx() {
  FX_KEYS.forEach((k) => {
    const r = document.querySelector('[data-fx="' + k + '"]');
    r.value = fx.params[k] || 0;
    r.nextElementSibling.textContent = r.value;
  });
  $("fxMirror").checked = !!fx.params.mirror;
  document.querySelectorAll(".preset-card").forEach((c) => {
    const on = c.dataset.preset === fx.preset;
    c.classList.toggle("active", on);
    c.setAttribute("aria-pressed", on);
  });
}

function pushFx() {
  clearTimeout(fxTimer);
  fxTimer = setTimeout(() => window.pywebview.api.set_effects(fx.params, fx.preset), 60);
}

function initFx(data) {
  fx = { params: data.params, preset: data.preset, presets: data.presets };
  FX_KEYS.forEach((k) => {
    document.querySelector('[data-fx="' + k + '"]').oninput = (e) => {
      fx.params[k] = Number(e.target.value);
      fx.preset = "";
      renderFx();
      pushFx();
    };
  });
  $("fxMirror").onchange = (e) => {
    fx.params.mirror = e.target.checked;
    fx.preset = "";
    renderFx();
    pushFx();
  };
  document.querySelectorAll(".preset-card").forEach((c) => {
    c.onclick = () => {
      fx.params = Object.assign({}, fx.presets[c.dataset.preset], { mirror: !!fx.params.mirror });
      fx.preset = c.dataset.preset;
      renderFx();
      pushFx();
    };
  });
  $("fxReset").onclick = () => {
    fx.params = Object.assign({}, fx.presets.original);
    fx.preset = "original";
    renderFx();
    pushFx();
  };
  renderFx();
}

function setFxBar(bar, pct) {
  let fill = bar.firstElementChild;
  if (!fill) {
    fill = document.createElement("span");
    fill.className = "fxbar-fill";
    bar.appendChild(fill);
  }
  const p = Math.max(0, Math.min(100, pct));
  fill.style.width = p > 0 ? "calc(max(" + p + "%, 12px) - 4px)" : "0";
}

function setRemoteText(text, fxName) {
  $("remoteState").textContent = text;
  const i = $("remoteFx");
  if (fxName) {
    i.src = "fx/" + fxName;
    i.classList.remove("hidden");
  } else {
    i.classList.add("hidden");
    i.removeAttribute("src");
  }
}

function markQuality() {
  document.querySelectorAll(".q-btn").forEach((b) => {
    b.classList.toggle("active", b.dataset.q === quality);
  });
}

function setRemoteUi(on) {
  remoteOn = on;
  $("remotePair").classList.toggle("hidden", !on);
  $("remoteBtn").textContent = on
    ? (S.remote_stop || "Stop remote")
    : (S.remote_start || "Start remote");
  $("toggleBtn").disabled = on;
  $("wifiIp").disabled = on;
  $("wifiKey").disabled = on;
}

window.flexRemote = function (state, detail) {
  if (!$("remoteState")) return;
  if (state === "starting") setRemoteText(S.remote_starting || "Starting tunnel...", "spinner.gif");
  else if (state === "ready") setRemoteText(S.remote_waiting || "Waiting for phone...", "");
  else if (state === "connected") setRemoteText(S.remote_connected || "Phone connected", "bolt.gif");
  else if (state === "stopped") setRemoteText("", "");
  else if (state === "error") {
    setRemoteText(S["remote_" + detail] || S.remote_failed || "Failed", "");
    setRemoteUi(false);
  }
};

function setUsb(connected) {
  $("usbDot").src = "fx/dot-" + (connected ? "online" : "off") + ".png";
  $("usbState").textContent = connected ? S.usb_connected : S.usb_disconnected;
}

function setPhoneApp(installed) {
  const label = $("installLabel");
  const btn = $("installBtn");
  if (installed) {
    label.textContent = S.phone_ready;
    btn.classList.remove("warn");
    btn.classList.add("ok");
  } else {
    label.textContent = S.btn_install;
    btn.classList.remove("ok");
  }
}

async function pollUsb() {
  try {
    const st = await window.pywebview.api.phone_status();
    setUsb(st.usb);
    setPhoneApp(st.app);
  } catch (e) {}
}

function setLangButton(langs, current) {
  const t = langs.find((l) => l[0] === current) || langs[0];
  $("langFlag").textContent = t[0].toUpperCase();
  $("langName").textContent = t[2];
}

function buildLangMenu(langs, current) {
  const menu = $("langMenu");
  menu.innerHTML = "";
  langs.forEach(([code, flag, name]) => {
    const item = document.createElement("div");
    item.className = "lang-item" + (code === current ? " active" : "");
    item.innerHTML =
      '<span class="lang-flag">' + code.toUpperCase() + "</span><span>" + name + "</span>";
    item.onclick = () => {
      $("langMenu").classList.add("hidden");
      setLang(code);
    };
    menu.appendChild(item);
  });
}

async function setLang(code) {
  const r = await window.pywebview.api.set_lang(code);
  S = r.strings;
  CFG.lang = r.lang;
  applyStrings();
  refreshVcam();
  setLangButton(CFG.langs, r.lang);
  buildLangMenu(CFG.langs, r.lang);
  pollUsb();
  if (lastState) setStatus(lastState, lastInfo);
}

function setStatus(state, info) {
  lastState = state;
  lastInfo = info;
  const pc = document.querySelector(".preview-card");
  if (pc) pc.classList.toggle("live", state === "connected");
  const dot = $("dot");
  dot.className = "dot " + (state || "");
  let text;
  if (state === "connected") text = (S.connected_fmt || "{}").replace("{}", info || "");
  else if (state === "error") text = S[info] || S.camera_generic || "Error";
  else if (state === "starting") text = S.status_starting || "Starting...";
  else if (state === "searching") text = S.status_searching || "Searching...";
  else if (state === "stopped") { text = S.status_stopped || "Stopped"; setRunning(false); }
  else text = S.status_ready || "Ready";
  $("statusText").textContent = text || (S.status_ready || "Ready");
}

function setRunning(on) {
  running = on;
  const b = $("toggleBtn");
  b.textContent = on ? S.btn_stop : S.btn_start;
  b.classList.toggle("running", on);
}

function setLog(text, cls) {
  const l = $("log");
  l.textContent = text || "";
  l.className = "log " + (cls || "");
}

function refreshVcam() {
  const label = $("obsLabel");
  const btn = $("obsBtn");
  if (CFG.vcam_ready) {
    label.textContent = S.vcam_ready;
    btn.classList.remove("warn");
    btn.classList.add("ok");
  } else {
    label.textContent = S.install_vcam;
    btn.classList.remove("ok");
    btn.classList.add("warn");
  }
  $("obsTile").innerHTML = icon(CFG.vcam_ready ? "webcam" : "triangle-alert", 18);
}

async function init() {
  const boot = await window.pywebview.api.get_bootstrap();
  S = boot.strings;
  CFG = boot;
  applyStrings();
  $("versionLbl").textContent = "v" + boot.version;
  $("trayChk").checked = !!boot.tray;
  refreshVcam();
  setRunning(boot.running);

  setLangButton(boot.langs, boot.lang);
  buildLangMenu(boot.langs, boot.lang);
  $("langBtn").onclick = (e) => {
    e.stopPropagation();
    $("langMenu").classList.toggle("hidden");
  };
  document.addEventListener("click", () => $("langMenu").classList.add("hidden"));

  $("collapseBtn").onclick = () => $("sidebar").classList.toggle("collapsed");
  document.querySelectorAll(".page-item").forEach((b) => {
    b.onclick = () => showPage(b.dataset.page);
  });
  $("settingsBack").onclick = () => showPage("home");
  $("discordChk").checked = boot.discord_rpc !== false;
  $("discordChk").onchange = (e) => window.pywebview.api.set_discord(e.target.checked);
  $("navGithub").onclick = () => window.pywebview.api.open_url(CFG.github);
  $("navDiscord").onclick = () => window.pywebview.api.open_url(CFG.discord);
  $("navInsta").onclick = () => window.pywebview.api.open_url(CFG.instagram);
  $("navDonate").onclick = () => window.pywebview.api.open_url(CFG.donate);
  $("obsBtn").onclick = async () => {
    if (CFG.vcam_ready) return;
    if (CFG.has_installer) {
      setLog(S.vcam_installing, "");
      const ok = await window.pywebview.api.install_virtualcam();
      if (ok) {
        CFG.vcam_ready = true;
        refreshVcam();
      }
    } else {
      window.pywebview.api.open_url(CFG.obs_url);
    }
  };
  $("trayChk").onchange = (e) =>
    window.pywebview.api.save_setting("tray", e.target.checked);

  $("toggleBtn").onclick = async () => {
    if (running) {
      window.pywebview.api.stop();
      setRunning(false);
    } else {
      const key = $("wifiKey").value.trim();
      if (key === "8474") {
        setStatus("error", "bad_key");
        return;
      }
      setRunning(true);
      setStatus("starting", null);
      window.pywebview.api.start($("wifiIp").value.trim(), key);
    }
  };

  document.querySelectorAll(".q-btn").forEach((b) => {
    b.onclick = () => {
      quality = b.dataset.q;
      markQuality();
      window.pywebview.api.remote_quality(quality);
    };
  });

  $("remoteBtn").onclick = async () => {
    if (remoteOn) {
      await window.pywebview.api.remote_stop();
      setRemoteUi(false);
      setRemoteText("", "");
      return;
    }
    $("remoteBtn").disabled = true;
    setRemoteText(S.remote_starting || "Starting tunnel...", "spinner.gif");
    $("remotePair").classList.remove("hidden");
    const r = await window.pywebview.api.remote_start(quality);
    $("remoteBtn").disabled = false;
    if (!r || !r.ok) {
      setRemoteText(S.remote_failed || "Could not start", "");
      $("remotePair").classList.add("hidden");
      return;
    }
    $("remoteQr").src = r.qr || "";
    $("remoteCode").textContent = r.code || "";
    setRemoteUi(true);
  };

  $("installBtn").onclick = async () => {
    setLog(S.installing, "");
    const r = await window.pywebview.api.install_apk();
    if (r.ok) setLog(S.install_ok, "ok");
    else if (r.key === "no_device") setLog(S.usb_debug_hint, "warn");
    else setLog(S.install_fail_fmt.replace("{}", S[r.key] || r.key), "err");
  };

  window.pywebview.api.check_update().then((u) => {
    if (u && u.has) {
      updateUrl = u.url;
      const b = $("updateBadge");
      b.textContent = S.update_available.replace("{}", u.latest);
      b.classList.remove("hidden");
      b.onclick = () => window.pywebview.api.open_url(u.url);
    }
  });

  pollUsb();
  setInterval(pollUsb, 3000);

  previewUrl = "http://127.0.0.1:8475/preview?t=" + encodeURIComponent(boot.preview_token);
  $("previewImg").src = previewUrl;
  $("wifiIp").value = boot.wifi_ip || "";
  $("wifiKey").value = boot.wifi_key || "";
  quality = boot.remote_quality || "medium";
  markQuality();
  applyTheme(boot.theme);
  applyMotion(boot.motion || "system");
  runIntro();
  $("aboutVersion").textContent = "v" + boot.version;
  initFx(boot.effects);
  $("aboutGithub").onclick = () => window.pywebview.api.open_url(CFG.github);
  document.querySelectorAll("#motionSeg button").forEach((b) => {
    b.onclick = () => {
      applyMotion(b.dataset.motion);
      window.pywebview.api.save_setting("motion", b.dataset.motion);
    };
  });
  document.querySelectorAll(".theme-card").forEach((d) => {
    d.onclick = () => {
      applyTheme(d.dataset.theme);
      window.pywebview.api.save_setting("theme", theme);
    };
  });
  setRunning(true);
  setStatus("starting", null);
  window.pywebview.api.start(boot.wifi_ip || "", boot.wifi_key || "");
  window.pywebview.api.whats_new().then((r) => r && showWhatsNew(r));
}

function setUpdate(state, pct, latest) {
  const b = $("updateBadge");
  if (!b) return;
  b.classList.remove("hidden");
  b.onclick = null;
  b.textContent = "";
  const fxImg = (src) => {
    const i = document.createElement("img");
    i.className = "fx";
    i.src = "fx/" + src;
    i.width = 16;
    i.height = 16;
    i.alt = "";
    return i;
  };
  const label = (t) => {
    const s = document.createElement("span");
    s.textContent = t;
    return s;
  };
  if (state === "downloading") {
    b.append(fxImg("arrow.gif"), label((S.update_downloading || "Downloading update {}%").replace("{}", pct)));
    const bar = document.createElement("span");
    bar.className = "fxbar";
    b.appendChild(bar);
    setFxBar(bar, pct);
  } else if (state === "waiting") {
    b.append(label(S.update_waiting || "Update ready, installs after streaming"));
  } else if (state === "installing") {
    b.append(fxImg("burst.gif"), label(S.update_installing || "Installing update..."));
  } else {
    b.append(label((S.update_available || "Update available: v{}").replace("{}", latest)));
    b.onclick = () => window.pywebview.api.open_url(updateUrl || CFG.github);
  }
}

function showWhatsNew(info) {
  $("whatsNewTitle").textContent = (S.whats_new || "What's new") + " — v" + info.version;
  $("whatsNewBody").textContent = info.notes;
  $("whatsNewClose").textContent = S.whats_new_close || "Got it";
  $("whatsNew").classList.remove("hidden");
  $("whatsNewClose").onclick = () => $("whatsNew").classList.add("hidden");
}

hydrateIcons();
window.flexStatus = setStatus;
window.flexUpdate = setUpdate;
window.addEventListener("pywebviewready", init);
setTimeout(() => { const i = $("intro"); if (i) i.remove(); }, 4500);
