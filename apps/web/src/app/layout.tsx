import type { Metadata, Viewport } from "next";
import "./globals.css";

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
      <body>{children}</body>
    </html>
  );
}
