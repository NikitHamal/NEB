import type { Program, Semester } from "./academics";

export enum UserRole {
    USER = "USER",
    MODERATOR = "MODERATOR",
    ADMIN = "ADMIN",
}

export interface User {
    id: number;
    clerkUserId: string;
    fullName: string;
    email: string;
    role: UserRole;
}

// ADMIN can do everything MODERATOR can, so gate on this instead of UserRole.MODERATOR alone.
export const isModeratorOrAdmin = (role?: UserRole): boolean =>
    role === UserRole.MODERATOR || role === UserRole.ADMIN;

export interface Profile {
    id: number;
    userId: number;
    bio?: string;
    programId?: number;
    semester?: Semester;
    college?: string;
    profilePictureUrl?: string;
}

interface ProfileWithProgram extends Profile {
    program?: Program;
}

export interface UserProfile extends User {
    profile: ProfileWithProgram;
}