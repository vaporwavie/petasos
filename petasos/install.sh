#!/usr/bin/env bash
# usage: petasos/install.sh
# Builds the Linux AppImage and installs it to ~/AppImages with a launcher entry, the layout Gear Lever uses.
set -euo pipefail

repo_root="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
cd "$repo_root"

[[ -d node_modules ]] || npm ci --no-audit --no-fund
npm run build
npx electron-builder --linux AppImage --publish never

version="$(node -p "require('./package.json').version")"
appimage="dist/petasos-$version-x86_64.AppImage"
target="$HOME/AppImages/petasos.appimage"
icon="$HOME/AppImages/.icons/petasos"
entry="$HOME/.local/share/applications/petasos.desktop"

mkdir -p "$(dirname "$icon")" "$(dirname "$entry")"
install -m 755 "$appimage" "$target"
install -m 644 build/icon.png "$icon"
cat > "$entry" <<DESKTOP
[Desktop Entry]
Type=Application
Name=Petasos
Comment=Desktop app for Hermes Agent
Icon=$icon
TryExec=$target
Exec=env DESKTOPINTEGRATION=1 $target %U
Terminal=false
Categories=Utility;
StartupWMClass=petasos
DESKTOP
update-desktop-database "$(dirname "$entry")" 2>/dev/null || true
echo "installed $target ($version)"
