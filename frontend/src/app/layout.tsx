import type { Metadata, Viewport } from "next";
import { Inter as FontSans } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/ui/theme-provider";
import Header from "@/components/ui/header";
import { cn } from "@/lib/utils";
import Footer from "@/components/ui/footer";
import { Toaster } from "@/components/ui/sonner";

const fontSans = FontSans({
  subsets: ["latin"],
  variable: "--font-sans",
});

const title = "Velocity AI";
const description =
  "An AI-powered Formula 1 chatbot delivering real-time race insights, driver stats, and team updates at lightning speed. Stay ahead of the competition with instant F1 knowledge! 🏎️⚡";

export const metadata: Metadata = {
  //Sets metadata for SEO and social media previews.
  metadataBase: new URL("https://github.com/sanjogbhalla16"),
  title,
  description,
  openGraph: {
    title,
    description,
  },
};

export const viewport: Viewport = {
  //Ensures the website is responsive.
  width: "device-width",
  initialScale: 1,
  minimumScale: 1,
  maximumScale: 1,
};

export default function RootLayout({
  //The children prop represents the page content.
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      // `next-themes` injects an extra classname to the body element to avoid
      // visual flicker before hydration. Hence the `suppressHydrationWarning`
      // prop is necessary to avoid the React hydration mismatch warning.
      // https://github.com/pacocoursey/next-themes?tab=readme-ov-file#with-app
      suppressHydrationWarning //Prevents hydration mismatch warnings caused by next-themes modifying the <body> class.
    >
      <body className={cn("font-sans antialiased", fontSans.variable)}>
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          <Header />
          {children}
          <Footer />
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}
