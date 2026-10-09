import type { Metadata } from "next";
import Console from "./console";

export const metadata: Metadata = {
  title: "Assessment console | Praeva by Dyplux",
  description:
    "Inspect dated pre-signing assessments, evidence, deterministic decisions and verifiable receipts.",
  alternates: { canonical: "https://praeva.dyplux.com/console/" },
};

export default function ConsolePage() {
  return <Console />;
}
