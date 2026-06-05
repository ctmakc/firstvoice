export const metadata = {
  title: "FirstVoice — AI-Native Digital Heritage for Indigenous Communities",
  description:
    "Community-controlled platform combining AI speech technology, Web3 provenance, and sacred governance to return data sovereignty to Indigenous and endangered-language communities.",
  keywords: [
    "indigenous language revitalization",
    "endangered languages",
    "AI speech",
    "Web3 provenance",
    "data sovereignty",
    "OCAP",
    "digital heritage",
  ],
  openGraph: {
    title: "FirstVoice — Community-Controlled Digital Heritage",
    description: "AI-native platform for Indigenous language preservation.",
    type: "website",
    url: "https://firstvoice.dev",
  },
  twitter: {
    card: "summary_large_image",
    title: "FirstVoice",
    description: "AI-native digital heritage platform.",
  },
};

import LandingPage from "@/components/LandingPage";

export default function Page() {
  return <LandingPage />;
}
