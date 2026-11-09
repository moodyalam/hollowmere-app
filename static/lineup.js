// The phone page: ask the app for the line-up every 10 seconds (plus a random
// 0-3 s, so a room full of phones doesn't hit the app at the same instant),
// and show the wristband, the sets, the version, or the apology.
(function () {
  const $ = (id) => document.getElementById(id);
  let revealed = false;
  let last = null;

  function setItem(set) {
    const li = document.createElement("li");
    li.className = "set" + (set.headliner ? " headliner" : "") + (set.backstage ? " backstage" : "");
    const time = document.createElement("span");
    time.className = "time";
    time.textContent = set.time;
    const body = document.createElement("div");
    const artist = document.createElement("p");
    if (set.headliner && !revealed) {
      artist.className = "mystery";
      artist.textContent = "? ? ? ? ?";
      artist.setAttribute("aria-label", "Secret headliner, not revealed yet");
    } else {
      artist.className = "artist";
      artist.textContent = set.artist;
    }
    const stage = document.createElement("span");
    stage.className = "stage";
    stage.textContent = set.stage;
    body.append(artist, stage);
    li.append(time, body);
    return li;
  }

  function show(data) {
    last = data;
    $("fest").textContent = data.festival;
    document.title = data.festival + ": your line-up";
    $("version").textContent = "v" + data.version;
    $("ticket").textContent = "№ " + data.ticket;
    $("tier").textContent = data.tier;
    $("band").classList.toggle("vip", data.tier === "VIP");
    $("sets").replaceChildren(...data.sets.map(setItem));
    $("sorry").hidden = true;
    $("today").hidden = false;
    $("reveal").hidden = revealed;
  }

  function status(text, waiting) {
    $("status-text").textContent = text;
    $("status").classList.toggle("waiting", Boolean(waiting));
  }

  async function refresh() {
    try {
      const reply = await fetch("/lineup?format=json", { headers: { Accept: "application/json" }, cache: "no-store" });
      if (reply.status === 500) {
        // The app answered, but something broke: show the reference it gave.
        const data = await reply.json().catch(() => ({}));
        $("reference").textContent = data.reference || "—";
        $("sorry").hidden = false;
        $("today").hidden = true;
        status("Trying again in a few seconds", true);
        return;
      }
      if (!reply.ok) throw new Error("HTTP " + reply.status);
      show(await reply.json());
      status("Live · updated " + new Date().toLocaleTimeString("en-GB"));
    } catch (error) {
      // No answer (the app is restarting, or the network dropped): keep the
      // last line-up on screen and say we're reconnecting.
      status("Reconnecting…", true);
    }
  }

  function loop() {
    refresh().finally(() => setTimeout(loop, 10000 + Math.random() * 3000));
  }

  $("reveal").addEventListener("click", () => {
    revealed = true;
    $("reveal").hidden = true;
    refresh();  // one extra request each: the "headliner reveal" spike
    if (last) show(last);
  });

  loop();
})();
