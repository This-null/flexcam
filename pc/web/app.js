let S = {};
let CFG = {};
let updateUrl = null;
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
}

function setUsb(connected) {
  $("usbDot").classList.toggle("on", !!connected);
  $("usbState").textContent = connected ? S.usb_connected : S.usb_disconnected;
}

function setPhoneApp(installed) {
  const label = $("installLabel");
  const btn = $("installBtn");
  if (installed) {
    label.textContent = "✓ " + S.phone_ready;
    btn.classList.remove("warn");
  } else {
    label.textContent = S.btn_install;
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
  $("langFlag").textContent = t[1];
  $("langName").textContent = t[2];
}

function buildLangMenu(langs, current) {
  const menu = $("langMenu");
  menu.innerHTML = "";
  langs.forEach(([code, flag, name]) => {
    const item = document.createElement("div");
    item.className = "lang-item" + (code === current ? " active" : "");
    item.innerHTML =
      '<span class="lang-flag">' + flag + "</span><span>" + name + "</span>";
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
    label.textContent = "✓ " + S.vcam_ready;
    btn.classList.remove("warn");
  } else {
    label.textContent = S.install_vcam;
    btn.classList.add("warn");
  }
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

  $("previewImg").src = "http://127.0.0.1:8475/preview";
  $("wifiIp").value = boot.wifi_ip || "";
  $("wifiKey").value = boot.wifi_key || "";
  setRunning(true);
  setStatus("starting", null);
  window.pywebview.api.start(boot.wifi_ip || "", boot.wifi_key || "");
}

function setUpdate(state, pct, latest) {
  const b = $("updateBadge");
  if (!b) return;
  b.classList.remove("hidden");
  b.onclick = null;
  if (state === "downloading") {
    b.textContent = (S.update_downloading || "Downloading update {}%")
      .replace("{}", pct);
  } else if (state === "waiting") {
    b.textContent = S.update_waiting || "Update ready — installs after streaming";
  } else if (state === "installing") {
    b.textContent = S.update_installing || "Installing update...";
  } else {
    b.textContent = (S.update_available || "Update available: v{}")
      .replace("{}", latest);
    b.onclick = () => window.pywebview.api.open_url(updateUrl || CFG.github);
  }
}

window.flexStatus = setStatus;
window.flexUpdate = setUpdate;
window.addEventListener("pywebviewready", init);
