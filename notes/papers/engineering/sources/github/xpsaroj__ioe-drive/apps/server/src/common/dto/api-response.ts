import type { PaginationMeta } from "../utils/pagination";

// A bare controller return value (not wrapped in this) becomes `data` with no message/meta.
export class ApiResponse<T> {
  private constructor(
    public readonly data: T,
    public readonly message?: string,
    public readonly meta?: PaginationMeta,
  ) {}

  static of<T>(data: T, message?: string, meta?: PaginationMeta): ApiResponse<T> {
    return new ApiResponse(data, message, meta);
  }
}
