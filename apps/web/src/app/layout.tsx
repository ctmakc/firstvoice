import type { Metadata, Viewport } from "next";
import "./globals.css";
import Nav from "@/components/Nav";

export const metadata: Metadata = {
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
  ],
  manifest: "/manifest.json",
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
