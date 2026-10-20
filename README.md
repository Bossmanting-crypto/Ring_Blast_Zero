# Ring Blast Zero for Wear OS

A standalone Wear OS app: a full-screen WebView running the watch build of
Ring Blast Zero (`app/src/main/assets/index.html`).

| | |
|---|---|
| App name | Ring Blast Zero |
| applicationId | `com.ringblastzero.game` |
| namespace | `com.ringblastzero.wear` |
| Version | 5.0.0-wear (versionCode 5000001) |
| Min / target | Wear OS 3 (API 30) / API 35 |

> The phone build must use the same `applicationId`, `com.ringblastzero.game`,
> and be signed with the same key. That pairing is what lets both ship under a
> single Play listing. Neither can change after the first upload.

## The watch build

Designed round-first for Wear OS rather than shrunk from the phone layout:

- Home: the board orbits as a dial with the time curved along the top bezel and
  RING · BLAST · ZERO along the bottom; a glowing Play button sits in the
  centre. One swipe or crown turn down shows the menu as Wear-style pill chips
  that shrink and fade toward the curved edges.
- Sector map: each sector is a clock face. Its 12 levels sit on the hour
  positions with the boss at 12 o'clock; swipe or turn the crown to move
  between sectors.
- Level, pause, results and game over: a round centrepiece, a curved title and
  a Wear OS edge button hugging the bottom of the screen.
- In play: a ring around the bezel fills toward two and three stars (or through
  the wave in endless); the score sits above the launcher, the level below it,
  and a pause tab on the bottom bezel.
- Boards are capped at three rings so nodes stay legible; sectors 4 and 5 keep
  their turning openings.
- Controls: tap anywhere to fire toward that point (or drag to aim and
  release). Tap the launcher, or turn the crown or rotating bezel, to swap the
  loaded node. The back button closes a screen, pauses or resumes; on the home
  screen it closes the app. Swipe-to-dismiss is off so horizontal drags can aim.
- Battery: 30 fps, true black around the content for OLED, a lighter sky, fewer
  particles and a slimmer music engine. Music is off by default
  (Settings > Music); sound effects and haptics are on. The screen stays on
  during a run only.
- Every size scales with the watch face, from small 192px screens to large
  260px ones.
- Dialogs are full-screen and round: the daily reward shows the 7-day streak as
  segments around the bezel with a Claim edge button; confirmations use round ✕
  and ✓ buttons. Back or the crown dismisses them.
- Crown on the home screen: one detent moves between the home page and the menu
  list, then it scrolls the list.

## Build

```bash
./make-keystore.sh          # once — use the phone app's key if it already has one
./gradlew bundleRelease     # app/build/outputs/bundle/release/app-release.aab
./gradlew assembleDebug     # sideloadable APK for a watch or emulator
```

Or open the folder in Android Studio (Koala or newer) and Run against a round
Wear OS emulator (API 33+) or a watch with ADB debugging on.

An `.aab` cannot be sideloaded. Use the debug APK for on-device testing:

```bash
adb -s <watch> install app/build/outputs/apk/debug/app-debug.apk
```

### CI

`.github/workflows/android.yml` builds and signs on GitHub. Add four
repository secrets — the same key as the phone app:

| Secret | Value |
|---|---|
| `KEYSTORE_BASE64` | `base64 -w0 upload-keystore.jks` |
| `KEYSTORE_PASSWORD` | store password |
| `KEY_ALIAS` | key alias |
| `KEY_PASSWORD` | key password |

The run log reports whether the bundle came out signed.

## Publishing

The watch app ships under the phone app's listing. In Play Console:
Release > Advanced settings > Form factors > add Wear OS, then upload this
bundle to the Wear OS track. Keep `versionCode` higher than the phone build's.
Wear screenshots (384x384) are in `store/`.

Wear OS apps must target API 35 or higher, which this project does.

## Updating the game

Rebuild the watch HTML from the game sources
(`python3 build.py watch index.html`) and copy it to
`app/src/main/assets/index.html`.

## Names left unchanged on purpose

- `SAVE_KEY = 'ringzero.save.v2'` — renaming it would discard existing players'
  progress for no visible benefit.
- `RZNative`, `window.rzRotary`, `window.rzBack` — the JS bridge symbols, which
  are matched by name in `MainActivity.kt`.
- The "Ring zero" achievement for clearing all 60 levels, which is wordplay on
  having zero rings left rather than the game's title.
- Contact details in the about and privacy screens still read
  `feedback@ringzero.game` and `@ringzero.bsky.social`. Update these to
  addresses you actually control before publishing — Play requires a working
  contact email.
