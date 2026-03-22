import type { Metadata } from "next";
import { Geist, Geist_Mono, Cormorant_Garamond } from "next/font/google";
import "./globals.css";
import KeepAlive from "@/components/KeepAlive";
import CustomCursor from "@/components/CustomCursor";
import ScrollProgress from "@/components/ScrollProgress";
import OpeningSequence from "@/components/OpeningSequence";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });
const cormorant = Cormorant_Garamond({
  variable: "--font-cormorant",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  style: ["normal", "italic"],
});

export const metadata: Metadata = {
  title: "Letterboxd Analytics — @burakxly",
  description: "Personal film analytics dashboard, auto-synced via GitHub bot.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable} ${cormorant.variable}`}>
      <body>
        <OpeningSequence />
        <CustomCursor />
        <ScrollProgress />
        <KeepAlive />
        {children}
      </body>
    </html>
  );
}
