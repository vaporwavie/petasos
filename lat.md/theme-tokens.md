# Theme tokens

Every renderer color, radius and font size comes from CSS custom properties in `main.css`, so the 12 themes and the squared-corners setting reach every screen.

## Default dark palette

The default dark theme's neutrals are tinted toward the navy accent, so its surfaces read as part of the brand rather than a stock gray.

Each surface and text token keeps the OKLCH lightness of the old neutral gray and takes a small chroma (0.005 to 0.011) at the accent's hue, 253. `--accent` stays `#003f7a`.

## Radius scale

Corners use `--radius-xs` (4px), `--radius-sm` (6px), `--radius-md` (10px), `--radius-lg` (14px) and `--radius-xl` (20px).

`html[data-radius="none"]`, set by [[src/renderer/src/components/ThemeProvider.tsx#ThemeProvider]] when rounded corners are off, zeroes all five tokens. Pills (`999px`), circles (`50%`) and the window-frame corners in [[window-chrome]] stay literal on purpose, so squared mode keeps toggles round and the chrome matches the OS window shape.

## Type scale

Font sizes use ten `--text-*` tokens from `--text-2xs` (10px) to `--text-4xl` (22px), with no half-pixel steps.

Display headings (32px and up, and the onboarding title's `clamp`) and the two 9px labels sized to fit an 18px shape stay literal. Weight 600 is reserved for headings, names and uppercase section labels; buttons, field labels, tabs and hints use 500.

## Syntax palette

The file viewer colors highlighted code from `--syntax-*` tokens scoped to `.file-viewer-modal`, with a dark default and a light set for the light, GitHub Light and Solarized Light themes.

The viewer's chrome uses the regular surface and text tokens on `--code-bg`, so it follows whichever theme is active instead of staying dark.

## Brand mark

The Petasos mark is a 32x32 pixel-art winged hat, drawn as a grid in [[scripts/brand/make_petasos.py]], which also renders every app icon.

The script writes `src/renderer/src/assets/petasos.svg` (one `<rect>` per pixel run, `crispEdges`) and the dark rounded tile `build/icon.svg`, then rasterizes the tile into `build/icon.png`, `build/icon.ico`, `build/icon.icns` and `resources/icon.png`. [[src/renderer/src/components/common/PetasosLogo.tsx#PetasosLogo]] renders the mark in the app; callers pick multiples of 16px so pixels stay square. The Hermes account sign-in keeps the upstream Hermes One mark, since it represents that service.

## Known token gaps

Two colors still have no semantic token: text on accent, success and error fills is a literal `#fff`, and info accents fall back to `#4aa8ff` through an undefined `--info`.

Kanban's running (teal) and review (purple) status hues are fixed on purpose, as described in [[kanban]].
