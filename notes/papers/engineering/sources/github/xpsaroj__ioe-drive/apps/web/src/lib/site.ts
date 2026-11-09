// Single source of truth for the site's public identity - reused by the root layout, robots.ts, and sitemap.ts.
export const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || "https://ioedrive.vercel.app";
export const SITE_NAME = "IOE Drive";
export const SITE_DESCRIPTION =
    "IOE Drive is a free, student-run platform for Institute of Engineering (IOE), Tribhuvan University students to browse, share, and download notes, past questions, assessments, and other academic resources by program, semester, and subject.";

export const DISCORD_CONTACTS = [
    { username: "indeed_sunil", href: "https://discord.com/users/1038303762235785216" },
    { username: "xpsaroj", href: "https://discord.com/users/1073637787934412882" },
] as const;
