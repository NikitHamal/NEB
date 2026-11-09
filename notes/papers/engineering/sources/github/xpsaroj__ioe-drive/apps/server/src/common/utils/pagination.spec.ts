import { buildPaginationMeta, getPaginationOffset } from "./pagination";

describe("getPaginationOffset", () => {
  it("returns 0 for the first page", () => {
    expect(getPaginationOffset(1, 10)).toBe(0);
  });

  it("skips one full page's worth of rows per page after the first", () => {
    expect(getPaginationOffset(2, 10)).toBe(10);
    expect(getPaginationOffset(3, 10)).toBe(20);
  });

  it("scales with a non-default limit", () => {
    expect(getPaginationOffset(4, 25)).toBe(75);
  });
});

describe("buildPaginationMeta", () => {
  it("computes totalPages by rounding up", () => {
    expect(buildPaginationMeta(1, 10, 25).totalPages).toBe(3);
  });

  it("floors totalPages at 1 even with zero results", () => {
    expect(buildPaginationMeta(1, 10, 0).totalPages).toBe(1);
  });

  it("flags hasNextPage/hasPrevPage correctly on a middle page", () => {
    const meta = buildPaginationMeta(2, 10, 30);

    expect(meta.hasPrevPage).toBe(true);
    expect(meta.hasNextPage).toBe(true);
  });

  it("flags hasNextPage false on the last page", () => {
    const meta = buildPaginationMeta(3, 10, 25);

    expect(meta.hasNextPage).toBe(false);
    expect(meta.hasPrevPage).toBe(true);
  });

  it("flags hasPrevPage false on the first page", () => {
    const meta = buildPaginationMeta(1, 10, 25);

    expect(meta.hasPrevPage).toBe(false);
  });

  it("echoes page/limit/total back unchanged", () => {
    const meta = buildPaginationMeta(2, 15, 40);

    expect(meta.page).toBe(2);
    expect(meta.limit).toBe(15);
    expect(meta.total).toBe(40);
  });
});
