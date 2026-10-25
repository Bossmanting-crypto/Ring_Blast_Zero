#!/usr/bin/env python3
"""Builds the phone game (phone/www/index.html) from the watch game (app/src/main/assets/index.html).

The game file holds both builds: phone styles, phone render code and a TARGET switch.
The watch file ships with TARGET='watch' and round watch layouts for six screens.
This script flips TARGET to 'phone' and swaps those six screens back to phone layouts,
so the phone and watch apps always run the same game version.

Run from the repo root:  python3 phone/make-phone-html.py
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "app/src/main/assets/index.html"
OUT = ROOT / "phone/www/index.html"

PHONE = {
"s-menu": """<section class="screen on" id="s-menu">
    <header class="profile">
      <button class="rank" data-go="trophies" aria-label="Your rank and trophies">
        <span class="rank-badge" id="m-rank">1</span>
        <span><b id="m-rankname">Cadet</b><span class="xpbar"><i id="m-xp"></i></span></span>
      </button>
      <div class="row" style="flex:none;gap:6px">
        <button class="chip" data-go="shop" aria-label="Coins, open shop"><span data-i="coin"></span><b class="coins">0</b></button>
        <button class="chip" data-go="shop" aria-label="Gems, open shop"><span data-i="gem"></span><b class="gems">0</b></button>
      </div>
    </header>
    <div class="menu-hero" id="menu-hero"><h1 class="logo">RING BLAST<br>ZERO<small>protect the core</small></h1></div>
    <div class="menu-actions">
      <button class="btn primary big" id="m-play"><span>Play</span><small id="m-play-sub">Level 1</small></button>
      <div class="menu-row">
        <button class="btn glass" id="m-endless"><span>Endless</span><small id="m-endless-sub"></small></button>
        <button class="btn glass" id="m-daily"><span>Daily orbit</span><small id="m-daily-sub"></small></button>
      </div>
      <div class="tiles">
        <button class="tile" data-go="missions"><span data-i="target"></span>Missions<i class="badge" id="b-missions"></i></button>
        <button class="tile" data-go="shop"><span data-i="bag"></span>Shop</button>
        <button class="tile" data-go="trophies"><span data-i="trophy"></span>Trophies</button>
        <button class="tile" data-go="settings"><span data-i="gear"></span>Settings</button>
      </div>
      <div class="menu-foot"><button class="link" data-go="levels">Sectors <span id="w-menu-stars"></span></button><button class="link" data-go="howto">How to play</button></div>
    </div>
  </section>""",

"s-levels": """<section class="screen dim" id="s-levels">
    <div class="sheet">
      <div class="sheet-head"><button class="round-btn" data-back aria-label="Back"><span data-i="back"></span></button><h2>Sectors</h2>
        <span class="chip sm"><span data-i="star" style="color:var(--amber)"></span><b id="lv-stars">0</b></span></div>
      <div class="sheet-body"><div class="sectors" id="lv-grid"></div></div>
    </div>
  </section>""",

"s-intro": """<section class="screen dim center" id="s-intro">
    <div class="sheet">
      <div class="sheet-head"><button class="round-btn" data-back aria-label="Back"><span data-i="back"></span></button><h2 id="i-title">Level 1</h2>
        <button class="chip link-chip" id="i-levels">Sectors</button></div>
      <div class="sheet-body">
        <div class="i-board"><img id="i-board" alt=""><div><b id="i-ring" style="display:block;font-size:16px"></b><small class="muted" id="i-ports"></small><small class="muted" id="w-i-best" hidden></small></div></div>
        <p class="i-tip" id="i-tip"></p>
        <div id="i-goals"></div>
        <div class="facts"><div class="swatches" id="i-swatches"></div><span class="muted small" id="i-count"></span></div>
        <div class="section-t" id="i-boost-t">Boosters</div>
        <div class="boosts" id="i-boosts"></div>
        <button class="btn primary big" id="i-start">Start</button>
      </div>
    </div>
  </section>""",

"s-pause": """<section class="screen dim center" id="s-pause">
    <div class="sheet narrow"><div class="sheet-body pad">
      <h2 class="big-title">Paused</h2>
      <p class="muted" id="p-sub"></p>
      <div class="stack">
        <button class="btn primary big" id="p-resume">Resume</button>
        <button class="btn glass" id="p-restart">Restart</button>
        <div class="row"><button class="btn glass" data-go="settings">Settings</button><button class="btn glass" data-go="howto">Help</button></div>
        <button class="btn glass" id="p-quit">Quit to menu</button>
      </div>
    </div></div>
  </section>""",

"s-result": """<section class="screen dim center" id="s-result">
    <div class="sheet narrow"><div class="sheet-body pad">
      <h2 class="big-title" id="r-title">Level clear</h2>
      <div class="bigstars" id="r-stars"><span data-i="star"></span><span data-i="star"></span><span data-i="star"></span></div>
      <div class="r-score" id="r-score">0</div>
      <div class="r-best" id="r-best"></div>
      <div class="r-stats" id="r-stats"></div>
      <div class="rewards" id="r-rewards"></div>
      <div class="stack">
        <button class="btn primary big" id="r-next">Next level</button>
        <div class="row"><button class="btn glass" id="r-retry">Retry</button><button class="btn glass" id="r-menu">Menu</button></div>
      </div>
    </div></div>
  </section>""",

"s-over": """<section class="screen dim center" id="s-over">
    <div class="sheet narrow"><div class="sheet-body pad">
      <h2 class="big-title danger-t" id="o-title">Core breached</h2>
      <p class="o-sub" id="o-sub"></p>
      <div class="r-score" id="o-score">0</div>
      <div class="r-best" id="o-best"></div>
      <div class="rewards" id="o-rewards"></div>
      <div class="stack">
        <button class="btn gold" id="o-revive"><span>Revive</span><small id="o-revive-sub"></small></button>
        <button class="btn primary" id="o-retry">Try again</button>
        <button class="btn glass" id="o-menu">Menu</button>
      </div>
    </div></div>
  </section>""",
}

def main():
    s = SRC.read_text(encoding="utf-8")
    flag = "const TARGET='watch', WATCH=TARGET==='watch';"
    if flag not in s:
        sys.exit("TARGET switch not found in the watch HTML; update make-phone-html.py")
    s = s.replace(flag, "const TARGET='phone', WATCH=TARGET==='watch';")
    for sid, html in PHONE.items():
        pat = re.compile(r'<section class="[^"]*" id="%s">.*?</section>' % sid, re.S)
        s, n = pat.subn(lambda m: html, s, count=1)
        if n != 1:
            sys.exit(f"Screen #{sid} not found in the watch HTML")
    # The watch UI block swaps in round renderers for the menu, sector map and level intro.
    # Keep the phone renderers by running that part only on the watch.
    a = s.find("/* Screens */\nconst _wMenu=Render.menu")
    b = s.find("/* In play: a ring around the bezel", a)
    if a < 0 or b < 0:
        sys.exit("Watch screen overrides not found; update make-phone-html.py")
    s = s[:a] + "if(WATCH){\n" + s[a:b] + "}\n" + s[b:]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(s, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(s):,} bytes)")

if __name__ == "__main__":
    main()
