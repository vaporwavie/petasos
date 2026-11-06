# Fork maintenance

Petasos is `fathah/hermes-desktop` under its own name. Only the desktop app is renamed. The Hermes Agent backend (`~/.hermes`, the `hermes` CLI) and the Hermes One account and inference provider keep their names, because the app talks to them.

The rename is small enough to carry as ordinary commits on `main`, so there's no generated branch like Rosewood's. Upstream merges straight in.

## What differs from upstream

- `electron-builder.yml`, `package.json`: app ID `io.github.vaporwavie.Petasos`, product name, artifact names, publish target.
- The app-name strings: `common.appName`, the welcome title and eyebrow, the window title, the Settings desktop row.
- `src/main/app/updater.ts`: packaged builds skip the update feed unless `PETASOS_UPDATE_FEED=1`. Petasos publishes no releases, and upstream's feed would replace it with Hermes One.
- `.github/workflows/petasos-sync.yml` and this folder.

Upstream's `release.yml` and `beta-release.yml` are disabled in the repo's Actions settings. They need upstream's signing secrets and only run on `release` and `beta` branches anyway.

## Build and install

```bash
petasos/install.sh
```

Builds the AppImage, copies it to `~/AppImages/petasos.appimage` with its icon in `~/AppImages/.icons/`, and writes `~/.local/share/applications/petasos.desktop`. That's the layout Gear Lever uses, so Gear Lever lists it next to Rosewood. Rerun it after every sync you want to use.

## Sync

The `Sync upstream` workflow merges upstream `main` into `main` daily at 06:00 UTC. It fails, leaving `main` alone, in two cases, and the run summary says which:

- Upstream and `main` changed the same lines.
- Upstream edited a file under `.github/workflows/`. The Actions token can't push workflow changes, so that merge has to come from a local clone.

Either way, run it locally:

```bash
git switch main && git pull && petasos/sync.sh && git push
```

GitHub's **Sync fork** button does the same merge. Never pick its **Discard commits** option, which drops the rename.
