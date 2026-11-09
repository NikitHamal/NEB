import { ProgramSummary } from "./academics.responses";
import { Semester, UserRole } from "../entities";

export interface ProfileSummary {
    id: number;
    userId: number;
    bio?: string;
    programId?: number;
    semester?: Semester;
    college?: string;
    profilePictureUrl?: string;
    program?: ProgramSummary;
}

export interface UploaderSummary {
    id: number;
    fullName: string;
    profile: {
        id: number;
        userId: number;
        profilePictureUrl?: string;
    };
}

export interface UserProfileSummary {
    id: number;
    fullName: string;
    createdAt: string;
    profile: ProfileSummary;
    upvoteCount: number;
}

/** The response shape of the admin role-change endpoint. */
export interface UserSummary {
    id: number;
    email: string | null;
    fullName: string;
    role: UserRole;
}