import type { Metadata, Viewport } from "next";
import "./globals.css";
import Nav from "@/components/Nav";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: "FirstVoice — Community-Controlled Heritage",
  description:
    "AI-native digital heritage platform returning data sovereignty to Indigenous and endangered-language communities.",
  keywords: [
    "indigenous",
    "language revitalization",
    "endangered languages",
    "AI",
    "oral history",
    "data sovereignty",
    "te reo Māori",
    "Web3",
    "blockchain provenance",
  ],
  manifest: "/manifest.json",
  openGraph: {
    title: "FirstVoice — Community-Controlled Digital Heritage",
    description:
      "AI speech technology + Web3 provenance + Sacred governance. Returning data sovereignty to Indigenous communities.",
    url: siteUrl,
    siteName: "FirstVoice",
    images: [
      {
        url: "https://raw.githubusercontent.com/ctmakc/firstvoice/master/screenshots/og-image.png",
        width: 1200,
        height: 630,
        alt: "FirstVoice — Community-Controlled Digital Heritage",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "FirstVoice — Community-Controlled Heritage",
    description:
      "AI-native platform for Indigenous language preservation. OCAP-by-design.",
    images: ["https://raw.githubusercontent.com/ctmakc/firstvoice/master/screenshots/og-image.png"],
  },
  authors: [{ name: "Maksym Stepanenko", url: "https://github.com/ctmakc" }],
  creator: "Maksym Stepanenko",
  publisher: "FirstVoice",
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  alternates: {
    canonical: siteUrl,
  },
};

export const viewport: Viewport = {
  themeColor: "#0a0a0a",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              if ('serviceWorker' in navigator) {
                window.addEventListener('load', () => {
                  navigator.serviceWorker.register('/sw.js').catch(console.error);
                });
              }
            `,
          }}
        />
      </head>
      <body style={{ paddingBottom: "4.5rem" }}>
        {children}
        <Nav />
      </body>
    </html>
  );
}
