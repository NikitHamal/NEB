import type { Metadata } from "next";
import Link from "next/link";

import { LegalDocument, type LegalSection } from "@/components/common/legal";

export const metadata: Metadata = {
    title: "Terms of Service",
    description: "The terms that govern using IOE Drive.",
};

const SECTIONS: LegalSection[] = [
    {
        id: "acceptance",
        heading: "Acceptance of Terms",
        body: (
            <p>
                By browsing or creating an account on IOE Drive, you agree to these terms. If you
                don&apos;t agree with them, please don&apos;t use the site.
            </p>
        ),
    },
    {
        id: "about-the-service",
        heading: "About the Service",
        body: (
            <p>
                IOE Drive is a free, collaborative platform for students of the Institute of
                Engineering (IOE), Tribhuvan University, to share and access academic resources.
                It&apos;s a personal project built and maintained by me and my friends -{" "}
                <strong>it is not an official IOE, Tribhuvan University, or Nepal government
                    service</strong>, and nothing on the site should be taken as an official
                position of IOE or the university.
            </p>
        ),
    },
    {
        id: "accounts",
        heading: "Accounts & Eligibility",
        body: (
            <p>
                You&apos;ll need an account, created via our authentication provider Clerk, to
                upload, use the marketplace, or message other users - browsing doesn&apos;t
                require one. You&apos;re responsible for keeping your account secure and for
                what happens under it. Program, semester, and college details on your profile
                are self-reported and not verified, so treat them as informational only. Don&apos;t
                impersonate another person, or create an account for anyone but yourself.
            </p>
        ),
    },
    {
        id: "your-content",
        heading: "Your Content",
        body: (
            <p>
                &quot;Your content&quot; means anything you upload or post: resource files,
                marketplace listings and photos, and messages. You keep ownership of what you
                contribute - by posting it, you give IOE Drive permission to host and display it
                to other users through the site&apos;s normal features. Only upload material you
                have the right to share, and don&apos;t upload anything harmful, like malware, or
                disguised as something it isn&apos;t.
            </p>
        ),
    },
    {
        id: "moderation",
        heading: "Content Moderation",
        body: (
            <p>
                We review content before it becomes visible to other users, and may remove
                anything that violates these terms.
            </p>
        ),
    },
    {
        id: "marketplace",
        heading: "Marketplace",
        body: (
            <p>
                The marketplace is strictly peer-to-peer: <strong>IOE Drive isn&apos;t a party to
                    any transaction</strong> {" "} between a buyer and seller, doesn&apos;t process
                payments, and doesn&apos;t handle delivery. Use your own judgment, and meet in
                safe, public places on campus when exchanging items.
            </p>
        ),
    },
    {
        id: "prohibited-conduct",
        heading: "Prohibited Conduct",
        body: (
            <ul>
                <li>Uploading content you don&apos;t have the right to share.</li>
                <li>Harassment, hate speech, or targeting other students.</li>
                <li>Posting spam, scams, or listings for illegal items.</li>
                <li>Attempting to compromise the platform&apos;s security.</li>
            </ul>
        ),
    },
    {
        id: "open-source",
        heading: "Open Source",
        body: (
            <p>
                IOE Drive&apos;s source code is publicly available on{" "}
                <a href="https://github.com/xpsaroj/ioe-drive/" target="_blank" rel="noopener noreferrer">
                    GitHub
                </a>{" "}
                under the MIT License, and contributions are welcome. That license covers the
                codebase itself - it&apos;s separate from the content users upload to the running
                site, which stays governed by the &quot;Your Content&quot; section above.
            </p>
        ),
    },
    {
        id: "disclaimers",
        heading: "Disclaimers",
        body: (
            <p>
                IOE Drive is provided &quot;as is,&quot; without warranty of any kind. Resources
                are shared by other students and aren&apos;t verified for accuracy by any official
                body - always cross-check against your course&apos;s official syllabus and
                instructor.
            </p>
        ),
    },
    {
        id: "liability",
        heading: "Limitation of Liability",
        body: (
            <p>
                To the fullest extent permitted by law, IOE Drive and its maintainers aren&apos;t
                liable for any indirect, incidental, or consequential damages arising from your
                use of the site.
            </p>
        ),
    },
    {
        id: "changes",
        heading: "Changes to These Terms",
        body: (
            <p>
                We may update these terms as the platform evolves. We&apos;ll update the
                &quot;Last updated&quot; date above whenever we do. Continuing to use IOE Drive
                after a change means you accept the updated terms.
            </p>
        ),
    },
    {
        id: "contact",
        heading: "Contact",
        body: (
            <p>
                Questions about these terms? Reach us through our <Link href="/contact">Contact page</Link>.
            </p>
        ),
    },
];

const TermsPage = () => (
    <LegalDocument
        title="Terms of Service"
        description="The ground rules for using IOE Drive - please read before you sign up."
        lastUpdated="August 14, 2026"
        sections={SECTIONS}
    />
);

export default TermsPage;
