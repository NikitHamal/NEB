export interface PaginationMeta {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
    hasNextPage: boolean;
    hasPrevPage: boolean;
}

export type ApiResponse<T> = Readonly<{
    success: true;
    data: T;
    message?: string;
    meta?: PaginationMeta;
} | {
    success: false;
    error: string;
}>;

export type EmptyApiResponse = ApiResponse<null>;

/** An `ApiResponse` for a paginated list endpoint - `data` is the page's items, `meta` is always present. */
export type PaginatedApiResponse<T> = Readonly<{
    success: true;
    data: T[];
    message?: string;
    meta: PaginationMeta;
} | {
    success: false;
    error: string;
}>;

export interface AsyncState<T> {
    data: T;
    loading: boolean;
    error: string | null;
}