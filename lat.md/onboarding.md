# Onboarding Chrome

The first-run screens (Welcome, Install) share one flat dark shell around the Petasos mark, provided by [[src/renderer/src/components/common/OnboardHero.tsx#OnboardHero]]. Titles are upright sans; the design intentionally runs dark regardless of theme.

The `.onboard-screen` CSS scope owns `color-scheme: dark`, its dark surface and text tokens, and its background colour. It never inherits saved light-theme tokens, so the first frame and every onboarding child retain the designed contrast. [[tests/onboarding-theme.test.ts]] protects that scope.

## OnboardHero

[[src/renderer/src/components/common/OnboardHero.tsx#OnboardHero]] renders the shared `onboard-*` chrome: a flat dark surface, the Petasos mark at 96px, an uppercase `eyebrow` label, an upright `title`, and page-specific `children`.

Everything renders on the first frame, so the user lands straight on the wizard with no intro animation.

Props: `eyebrow`, `title`, `children`, `wide` (widen the column for the installing terminal). All visual tokens live under the `ONBOARDING HERO (shared)` block in `main.css`; `.onboard-screen` also scopes a brighter navy `--accent` so the primary button reads on the dark surface. The shell carries no glows, gradients, blur, particles or entrance motion.

The screens are `user-select: none` chrome; only `input`, `textarea`, `code`, and `[data-selectable]` stay selectable (so the install path and log can still be copied).

## Welcome

[[src/renderer/src/screens/Welcome/Welcome.tsx#Welcome]] is the default first-run view. Its no-error state renders through `OnboardHero`.

The hero carries the "PETASOS" eyebrow, subtitle, a flat accent "Get Started" pill, and bordered `.onboard-btn-secondary` "Connect via SSH" / "Connect to Remote Hermes" pills. The install-error state and the SSH / remote connect panels keep the legacy `.welcome-screen` layout.

## Install confirm + progress

[[src/renderer/src/screens/Install/Install.tsx#Install]] renders both the pre-install confirmation and the running progress through `OnboardHero`.

The confirm view (eyebrow "SETUP", title "Before installing") shows the target path in an `.onboard-field`, a `.onboard-note-card` describing the fresh/update/replace state, and Install / Use-existing / Cancel actions.

The progress view (`wide`) shows phase labels and an indeterminate bar while work is running; successful completion reaches 100 percent (see [[desktop-updates#Agent phases]]). It then shows then a **fixed-size** terminal log window (`.onboard-terminal`): its body has a constant height and scrolls internally, so streaming log lines never reflow the surrounding layout. The log auto-scrolls to the newest line.

Unix execution follows the [[desktop-security#Runtime security#Verified Unix bootstrap|verified bootstrap boundary]] before running downloaded code.

### Existing-install environment handoff

An adopted install wins over the exact inherited `HERMES_HOME` active during selection, preventing restart loops while preserving a different later environment override.

[[src/main/installer.ts#setHermesHomeOverride]] records a one-way fingerprint of that shadowed environment value beside the selected home. On restart, a matching fingerprint activates the saved selection only while it remains a desktop-compatible install; absent, legacy, incomplete, and later-different values keep the existing precedence.

[[tests/installer-home-override.test.ts]] covers the same-environment handoff, launch-time capture, cleartext-path minimization, legacy precedence, absent environments, later-different environments, deleted selections, and incomplete installs.

### Single-run installation

After confirmation, one mounted install screen starts exactly one installer run even if the active locale changes while that run is pending.

The running effect is keyed only by its phase. A current translation reference supplies localized fallback errors without making translation identity an effect dependency, which prevents language changes from restarting installation. [[src/renderer/src/screens/Install/Install.test.tsx]] covers the invariant.

## Startup splash

The very first frame on launch is still [[src/renderer/src/screens/SplashScreen/SplashScreen.tsx]], shown by [[src/renderer/src/App.tsx#App]] while `runInstallCheck` runs. It is separate from the onboarding chrome above — see [[main-process]] for its "Switch to local mode" escape hatch.

It shows the petasos mark and a status line on black, with no background video and no minimum hold, so it leaves as soon as the check settles.
