# Petasos

Petasos started as `fathah/hermes-desktop` and split off at upstream `17102486` (2026-10-13). It no longer merges upstream. Only the desktop app is renamed. The Hermes Agent backend (`~/.hermes`, the `hermes` CLI) and the Hermes One account and inference provider keep their names, because the app talks to them.

The app is a frontend for Hermes, so the part that has to stay current is the agent, not upstream's desktop code. An upstream fix worth having gets cherry-picked from the `upstream` remote by hand.

## Where Petasos departs from upstream

- `electron-builder.yml`, `package.json`: app ID `io.github.vaporwavie.Petasos`, product name, artifact names, publish target.
- The app-name strings: `common.appName`, the welcome title and eyebrow, the window title, the Settings desktop row.
- `src/main/app/updater.ts`: packaged builds skip the update feed unless `PETASOS_UPDATE_FEED=1`. Petasos publishes no releases, and upstream's feed would replace it with Hermes One.
- The Office tab is gone, along with everything only it used: the Claw3D main process, the Kanban HQ board, the bank-teller wallet actions, the GPU banner's re-enable IPC, and the Three.js dependencies.

Upstream's `release.yml` and `beta-release.yml` are disabled in the repo's Actions settings. They need upstream's signing secrets and only run on `release` and `beta` branches anyway.

## Keeping Hermes current

Settings > About shows the Hermes Agent card. It reads `hermes version`, flags an update when the CLI reports one, and its update button runs `hermes update`. From a terminal, `hermes update` does the same.

## Build and install

```bash
petasos/install.sh
```

Builds the AppImage, copies it to `~/AppImages/petasos.appimage` with its icon in `~/AppImages/.icons/`, and writes `~/.local/share/applications/petasos.desktop`. That's the layout Gear Lever uses, so Gear Lever lists it next to Rosewood. Rerun it after changes you want to use.
