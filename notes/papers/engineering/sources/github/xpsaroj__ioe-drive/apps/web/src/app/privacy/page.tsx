import type { Metadata } from "next";
import Link from "next/link";

import { LegalDocument, type LegalSection } from "@/components/common/legal";

export const metadata: Metadata = {
    title: "Privacy Policy",
    description: "How IOE Drive collects, uses, and protects your information.",
};

const SECTIONS: LegalSection[] = [
    {
        id: "overview",
        heading: "Overview",
        body: (
            <p>
                IOE Drive is a free, student-run platform for Institute of Engineering (IOE),
                Tribhuvan University students to share and access academic resources. It&apos;s a
                personal project built by me and my friends, not an official IOE product. This
                policy explains what information we collect, why we collect it, and how it&apos;s
                protected.
            </p>
        ),
    },
    {
        id: "information-we-collect",
        heading: "Information We Collect",
        body: (
            <>
                <p>We collect only what&apos;s needed to run the site:</p>
                <ul>
                    <li>
                        <strong>Account details</strong>, handled by our authentication provider,
                        Clerk: your name and email address.
                    </li>
                    <li>
                        <strong>Profile details you choose to add</strong>, like a short bio, your
                        program, semester, and college. These are self-reported - we don&apos;t
                        verify them.
                    </li>
                    <li>
                        <strong>Content you contribute</strong>, like resource files, marketplace
                        listings, and messages to other students.
                    </li>
                    <li>
                        <strong>Basic, cookieless analytics</strong> via Vercel Analytics -
                        aggregate page-view counts, not tied to your identity or account.
                    </li>
                    <li>
                        <strong>Basic technical logs</strong> kept by our hosting providers, used
                        only for security and debugging - never for tracking you across the web.
                    </li>
                </ul>
            </>
        ),
    },
    {
        id: "what-we-dont-collect",
        heading: "What We Don't Collect",
        body: (
            <p>
                IOE Drive carries no advertising, no cross-site tracking, and no marketing
                cookies. We don&apos;t sell, rent, or trade your information to anyone, for any
                reason. The one analytics tool we do use, Vercel Analytics, is cookieless and only
                reports aggregate page views - it doesn&apos;t build a profile of you or follow
                you elsewhere.
            </p>
        ),
    },
    {
        id: "cookies-and-local-storage",
        heading: "Cookies & Local Storage",
        body: (
            <ul>
                <li>A session cookie to keep you signed in between visits.</li>
                <li>Your theme preference (light, dark, or system), saved locally in your browser. It never leaves your device.</li>
                <li>Vercel Analytics (see above) sets no cookies at all - it just counts page views in aggregate.</li>
            </ul>
        ),
    },
    {
        id: "how-we-use-it",
        heading: "How We Use Your Information",
        body: (
            <ul>
                <li>To operate the core features: browsing, uploading, the marketplace, and messaging.</li>
                <li>To personalize your experience, like defaulting to your program and semester once you&apos;ve set them.</li>
                <li>To keep the platform safe and prevent abuse.</li>
            </ul>
        ),
    },
    {
        id: "who-we-share-with",
        heading: "Who We Share It With",
        body: (
            <p>
                We rely on a small number of trusted service providers to run authentication,
                store your files, and host the site. Each only receives what it needs to do its
                job, and none are allowed to use your data for their own purposes. We never share
                your information with advertisers or data brokers, and we never sell it.
            </p>
        ),
    },
    {
        id: "data-retention",
        heading: "Data Retention",
        body: (
            <p>
                We keep your account and content for as long as your account exists. If you
                delete something, it&apos;s removed right away.
            </p>
        ),
    },
    {
        id: "your-rights",
        heading: "Your Rights & Choices",
        body: (
            <p>
                You&apos;re in control of your own content and can update or remove most of it
                yourself, anytime. If you&apos;d like your account and all associated data fully
                removed, reach out through our <Link href="/contact">Contact page</Link> {" "} and
                we&apos;ll take care of it.
            </p>
        ),
    },
    {
        id: "changes",
        heading: "Changes to This Policy",
        body: (
            <p>
                IOE Drive is still actively being built, and this policy may change as it grows.
                We&apos;ll update the &quot;Last updated&quot; date above whenever it does.
            </p>
        ),
    },
    {
        id: "contact",
        heading: "Contact Us",
        body: (
            <p>
                Questions about this policy, or a request about your data? See our{" "}
                <Link href="/contact">Contact page</Link> for the fastest way to reach us.
            </p>
        ),
    },
];

const PrivacyPage = () => (
    <LegalDocument
        title="Privacy Policy"
        description="What we collect, why we collect it, and how it's protected - in plain language."
        lastUpdated="August 14, 2026"
        sections={SECTIONS}
    />
);

export default PrivacyPage;
