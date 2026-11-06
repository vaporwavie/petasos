import mark from "../../assets/petasos.svg";

// The mark is a 32px pixel grid; multiples of 16px keep every pixel square.
function PetasosLogo({ size = 32 }: { size?: number }): React.JSX.Element {
  return <img src={mark} width={size} height={size} alt="Petasos" />;
}

export default PetasosLogo;
