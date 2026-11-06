import type { ReactNode } from "react";
import PetasosLogo from "./PetasosLogo";

interface OnboardHeroProps {
  eyebrow: string;
  title: ReactNode;
  children?: ReactNode;
  // Widen the content column (installing progress / terminal log).
  wide?: boolean;
}

/**
 * Shared chrome for the onboarding screens: the emblem, eyebrow, upright
 * title, and the page-specific `children`, all visible on the first frame.
 */
function OnboardHero({
  eyebrow,
  title,
  children,
  wide = false,
}: OnboardHeroProps): React.JSX.Element {
  return (
    <div className="screen onboard-screen">
      <div className={`onboard-hero${wide ? " onboard-hero--wide" : ""}`}>
        <div className="onboard-emblem">
          <PetasosLogo size={96} />
        </div>

        <div className="onboard-eyebrow">{eyebrow}</div>
        <h1 className="onboard-title">{title}</h1>
        <div className="onboard-body">{children}</div>
      </div>
    </div>
  );
}

export default OnboardHero;
