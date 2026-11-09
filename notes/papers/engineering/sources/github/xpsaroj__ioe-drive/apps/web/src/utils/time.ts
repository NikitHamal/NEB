import { formatDistanceToNow } from "date-fns";

export const getRelativeTime = (date: string) => {
    return formatDistanceToNow(new Date(date), { addSuffix: true });
};