import React from "react";
import clsx from "clsx";

export type BadgeVariant =
    | "default"
    | "primary"
    | "secondary"
    | "success"
    | "error"
    | "warning"
    | "info";

export type BadgeSize = "sm" | "md" | "lg";

export interface BadgeProps {
    variant?: BadgeVariant;
    size?: BadgeSize;
    /** Overrides `variant` with explicit colors. */
    color?: {
        bg: string;
        text: string;
        border?: string;
    };
    dot?: boolean;
    outline?: boolean;
    icon?: React.ReactNode;
    /** Shows a remove (X) button that calls this when clicked. */
    onRemove?: () => void;
    className?: string;
    children: React.ReactNode;
}

const variantStyles: Record<BadgeVariant, { bg: string; text: string; border: string }> = {
    default: {
        bg: "bg-badge-background",
        text: "text-badge-foreground",
        border: "border-badge-border",
    },
    primary: {
        bg: "bg-foreground",
        text: "text-foreground-inverse",
        border: "border-foreground",
    },
    secondary: {
        bg: "bg-background-tertiary",
        text: "text-foreground-secondary",
        border: "border-border-secondary",
    },
    success: {
        bg: "bg-badge-success",
        text: "text-badge-success-text",
        border: "border-success",
    },
    error: {
        bg: "bg-badge-error",
        text: "text-badge-error-text",
        border: "border-error",
    },
    warning: {
        bg: "bg-badge-warning",
        text: "text-badge-warning-text",
        border: "border-warning",
    },
    info: {
        bg: "bg-badge-info",
        text: "text-badge-info-text",
        border: "border-info",
    },
};

const sizeStyles: Record<BadgeSize, string> = {
    sm: "text-xs px-2 py-0.5 gap-1",
    md: "text-sm px-2.5 py-1 gap-1.5",
    lg: "text-sm px-3 py-1.5 gap-2",
};

const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
    (
        {
            variant = "default",
            size = "md",
            color,
            dot = false,
            outline = false,
            icon,
            onRemove,
            className,
            children,
            ...props
        },
        ref
    ) => {
        const styles = color
            ? {
                  bg: color.bg,
                  text: color.text,
                  border: color.border || color.bg,
              }
            : variantStyles[variant];

        return (
            <span
                ref={ref}
                className={clsx(
                    "inline-flex items-center font-medium rounded-md border whitespace-nowrap",
                    sizeStyles[size],
                    outline ? `${styles.border} ${styles.text} bg-transparent` : `${styles.bg} ${styles.text} ${styles.border}`,
                    className
                )}
                {...props}
            >
                {dot && (
                    <span
                        className={clsx(
                            "w-1.5 h-1.5 rounded-full",
                            outline ? styles.text.replace("text-", "bg-") : "bg-current"
                        )}
                    />
                )}
                {icon && <span className="inline-flex items-center">{icon}</span>}
                <span>{children}</span>
                {onRemove && (
                    <button
                        type="button"
                        onClick={(e) => {
                            e.stopPropagation();
                            onRemove();
                        }}
                        className="inline-flex items-center hover:opacity-70 transition-opacity ml-1"
                        aria-label="Remove"
                    >
                        <svg
                            className="w-3 h-3"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M6 18L18 6M6 6l12 12"
                            />
                        </svg>
                    </button>
                )}
            </span>
        );
    }
);

Badge.displayName = "Badge";

export default Badge;
