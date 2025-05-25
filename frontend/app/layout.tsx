import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { vazirMatn } from 'next-persian-fonts/vazirmatn'
import { MyRuntimeProvider } from "@/app/MyRuntimeProvider";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Compliance Assistant",
  description: "Compliance AI Assistant",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <MyRuntimeProvider>
      <html lang="en">
        <body
          className={`${vazirMatn.className} ${geistSans.variable} ${geistMono.variable} antialiased`}
        >
          {children}
        </body>
      </html>
    </MyRuntimeProvider>
  );
}
