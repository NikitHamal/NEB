import type { Metadata } from "next";
import { Analytics } from "@vercel/analytics/next"
import { IBM_Plex_Sans, IBM_Plex_Mono } from "next/font/google";

import "./globals.css";
import { ThemeProvider } from "@/providers/theme-provider";
import { MotionProvider } from "@/providers/motion-provider";
import { ClerkThemeProvider } from "@/providers/clerk-theme-provider";
import { ClerkApiProvider } from "@/providers/ClerkApiProvider";
import { QueryProvider } from '@/providers/query-provider';
import { AuthStateWatcher } from "@/providers/AuthStateWatcher";
import { AppDataInitializer } from "@/providers/AppDataInitializer";
import { MessagingSocketProvider } from "@/providers/MessagingSocketProvider";
import { NotificationsSocketProvider } from "@/providers/NotificationsSocketProvider";

import { GlobalLoader, LayoutWrapper } from "@/components/layout";
import { SITE_DESCRIPTION, SITE_NAME, SITE_URL } from "@/lib/site";

// Body copy and headings - see --font-sans in globals.css.
const plexSans = IBM_Plex_Sans({ subsets: ["latin"], weight: ["400", "500", "600", "700"], variable: "--font-plex-sans" });
// Used sparingly for the wordmark and nav "eyebrow" labels (see --font-display in globals.css) - not applied globally.
const plexMono = IBM_Plex_Mono({ subsets: ["latin"], weight: ["500", "600"], variable: "--font-plex-mono" });

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: `${SITE_NAME} - Academic Resources for IOE Students`,
    template: `%s | ${SITE_NAME}`,
  },
  description: SITE_DESCRIPTION,
  keywords: [
    "IOE", "Institute of Engineering", "Tribhuvan University", "IOE notes",
    "IOE past questions", "IOE Drive", "engineering notes Nepal", "IOE Pulchowk",
    "IOE Thapathali", "IOE syllabus",
  ],
  openGraph: {
    title: SITE_NAME,
    description: SITE_DESCRIPTION,
    url: "/",
    siteName: SITE_NAME,
    images: [{ url: "/images/home/logo.png", width: 283, height: 303, alt: SITE_NAME }],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary",
    title: SITE_NAME,
    description: SITE_DESCRIPTION,
    images: ["/images/home/logo.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`bg-background text-foreground min-h-screen ${plexSans.className} ${plexMono.variable}`}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
          <MotionProvider>
            <ClerkThemeProvider>
              <ClerkApiProvider>
                <QueryProvider>
                  <AuthStateWatcher>
                    <MessagingSocketProvider>
                      <NotificationsSocketProvider>
                        <AppDataInitializer>
                          <GlobalLoader>
                            <LayoutWrapper>
                              {children}
                            </LayoutWrapper>
                          </GlobalLoader>
                        </AppDataInitializer>
                      </NotificationsSocketProvider>
                    </MessagingSocketProvider>
                  </AuthStateWatcher>
                </QueryProvider>
              </ClerkApiProvider>
            </ClerkThemeProvider>
          </MotionProvider>
        </ThemeProvider>

        <Analytics />
      </body>
    </html>
  );
}
