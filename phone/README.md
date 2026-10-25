# Ring Blast Zero: phone build

The Android phone app. It ships under the same Play listing as the watch app in `../app`.

| | |
|---|---|
| App name | Ring Blast Zero |
| applicationId | `com.ringblastzero.game` (same as the watch build) |
| Version | 5.0.0 (versionCode 5000000) |
| Min / target | Android 7.0 (API 24) / API 36 |
| Wrapper | Capacitor 8 |

## Where the game comes from

There is one game file: the watch app's `app/src/main/assets/index.html`. It already
contains the phone styles and phone code, behind a `TARGET` switch.

`make-phone-html.py` turns it into `www/index.html` for phones:

- sets `TARGET` to `'phone'`
- puts the phone layouts back for six screens: menu, sectors, level intro, pause,
  results and game over (the watch file has round layouts there)
- keeps the watch's round renderers from replacing the phone ones

Nothing in the watch files is changed. When you update the game, update the watch HTML as
usual, then run `npm run sync` here (CI does this on every build), and the phone app picks
up the same version.

## Build

```bash
cd phone
npm install
npm run sync        # makes www/index.html and copies it into the Android project
npm run open        # opens Android Studio
npm run build:aab   # android/app/build/outputs/bundle/release/app-release.aab
npm run build:apk   # debug APK to sideload on a phone
```

Needs Node 22+ and Android Studio with SDK Platform 36.

## CI

`.github/workflows/phone-android.yml` builds on every push that touches `phone/` or the
game file. It uses the **same four secrets** as the watch build (`KEYSTORE_BASE64`,
`KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD`), so both apps are signed with one key.

Artifacts: `ring-blast-zero-phone-aab` (upload to Play) and `ring-blast-zero-phone-apk`
(sideload to test).

## Version codes

Phone and watch share one listing, so their version codes must never collide. Keep the
phone **below** the watch:

| Build | versionCode | File |
|---|---|---|
| Phone | 5000000 | `phone/android/app/build.gradle` |
| Watch | 5000001 | `app/build.gradle.kts` |

For each new release, raise both, for example phone 5000002 and watch 5000003.

## Icons and splash

Made from the game's own menu ring and kept in `assets/`. To regenerate:

```bash
npx capacitor-assets generate --android --iconBackgroundColor '#05060f' --splashBackgroundColor '#05060f'
```

## Before publishing

The about and privacy screens still say `feedback@ringzero.game` and
`@ringzero.bsky.social`. Change them in the watch HTML (the phone build copies them) to
contacts you control.
