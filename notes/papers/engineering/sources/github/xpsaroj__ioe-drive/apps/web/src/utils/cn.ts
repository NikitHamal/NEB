import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

// Combines Tailwind classes and merges conflicts - last one wins.
export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}