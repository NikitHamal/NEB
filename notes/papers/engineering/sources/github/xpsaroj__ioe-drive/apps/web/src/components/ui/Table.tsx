"use client";

import React from "react";
import clsx from "clsx";
import { Inbox } from "lucide-react";

export interface Column<T> {
    key: string;
    label: string;
    render?: (item: T, index: number) => React.ReactNode;
    align?: "left" | "center" | "right";
    sortable?: boolean;
    width?: string;
}

export interface TableProps<T> {
    data: T[];
    columns: Column<T>[];
    striped?: boolean;
    hoverable?: boolean;
    onRowClick?: (item: T, index: number) => void;
    loading?: boolean;
    emptyMessage?: string;
    sortable?: boolean;
    className?: string;
    tableClassName?: string;
}

function Table<T>({
    data,
    columns,
    striped = false,
    hoverable = true,
    onRowClick,
    loading = false,
    emptyMessage = "No data available",
    sortable = false,
    className,
    tableClassName,
}: TableProps<T>) {
    const [sortConfig, setSortConfig] = React.useState<{
        key: string;
        direction: "asc" | "desc";
    } | null>(null);

    const sortedData = React.useMemo(() => {
        if (!sortConfig || !sortable) return data;

        return [...data].sort((a, b) => {
            const aValue = (a as Record<string, unknown>)[sortConfig.key];
            const bValue = (b as Record<string, unknown>)[sortConfig.key];

            if (aValue == null) return 1;
            if (bValue == null) return -1;

            if (aValue < bValue) {
                return sortConfig.direction === "asc" ? -1 : 1;
            }
            if (aValue > bValue) {
                return sortConfig.direction === "asc" ? 1 : -1;
            }
            return 0;
        });
    }, [data, sortConfig, sortable]);

    const handleSort = (columnKey: string, columnSortable?: boolean) => {
        if (!sortable || !columnSortable) return;

        setSortConfig((current) => {
            if (current?.key === columnKey) {
                return {
                    key: columnKey,
                    direction: current.direction === "asc" ? "desc" : "asc",
                };
            }
            return { key: columnKey, direction: "asc" };
        });
    };

    const getAlignClass = (align?: "left" | "center" | "right") => {
        switch (align) {
            case "center":
                return "text-center";
            case "right":
                return "text-right";
            default:
                return "text-left";
        }
    };

    if (loading) {
        return (
            <div className={clsx("w-full overflow-auto rounded-lg border border-border", className)}>
                <table className={clsx("w-full text-sm", tableClassName)}>
                    <thead className="bg-background-tertiary border-b border-border">
                        <tr>
                            {columns.map((column) => (
                                <th
                                    key={column.key}
                                    className={clsx(
                                        "px-4 py-3 font-display font-medium text-foreground-secondary text-xs uppercase tracking-wide",
                                        getAlignClass(column.align)
                                    )}
                                    style={{ width: column.width }}
                                >
                                    {column.label}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {Array.from({ length: 5 }).map((_, idx) => (
                            <tr key={idx} className="border-b border-border">
                                {columns.map((column) => (
                                    <td
                                        key={column.key}
                                        className={clsx("px-4 py-3", getAlignClass(column.align))}
                                    >
                                        <div className="h-4 bg-skeleton-base animate-pulse rounded" />
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        );
    }

    return (
        <div className={clsx("w-full overflow-auto rounded-lg border border-border", className)}>
            <table className={clsx("w-full text-sm", tableClassName)}>
                <thead className="bg-background-tertiary border-b border-border">
                    <tr>
                        {columns.map((column) => (
                            <th
                                key={column.key}
                                className={clsx(
                                    "px-4 py-3 font-display font-medium text-foreground-secondary text-xs uppercase tracking-wide whitespace-nowrap",
                                    getAlignClass(column.align),
                                    column.sortable && sortable && "cursor-pointer select-none hover:text-foreground"
                                )}
                                style={{ width: column.width }}
                                onClick={() => handleSort(column.key, column.sortable)}
                            >
                                <div className="flex items-center gap-2">
                                    {column.label}
                                    {column.sortable && sortable && (
                                        <span className="text-foreground-muted">
                                            {sortConfig?.key === column.key
                                                ? sortConfig.direction === "asc"
                                                    ? "↑"
                                                    : "↓"
                                                : "↕"}
                                        </span>
                                    )}
                                </div>
                            </th>
                        ))}
                    </tr>
                </thead>

                <tbody>
                    {sortedData.length === 0 ? (
                        <tr>
                            <td
                                colSpan={columns.length}
                                className="px-4 py-12 text-foreground-muted"
                            >
                                <div className="flex flex-col items-center gap-2">
                                    <Inbox className="size-5 text-foreground-tertiary" />
                                    <p className="text-center">{emptyMessage}</p>
                                </div>
                            </td>
                        </tr>
                    ) : (
                        sortedData.map((item, rowIndex) => (
                            <tr
                                key={rowIndex}
                                className={clsx(
                                    "border-b border-border last:border-b-0 transition-colors",
                                    hoverable && "hover:bg-background-hover",
                                    onRowClick && "cursor-pointer",
                                    striped && rowIndex % 2 === 1 && "bg-background-secondary"
                                )}
                                onClick={() => onRowClick?.(item, rowIndex)}
                            >
                                {columns.map((column) => (
                                    <td
                                        key={column.key}
                                        className={clsx(
                                            "px-4 py-3 text-foreground",
                                            getAlignClass(column.align)
                                        )}
                                    >
                                        {column.render
                                            ? column.render(item, rowIndex)
                                            : String((item as Record<string, unknown>)[column.key] ?? "")}
                                    </td>
                                ))}
                            </tr>
                        ))
                    )}
                </tbody>
            </table>
        </div>
    );
}

export default Table;