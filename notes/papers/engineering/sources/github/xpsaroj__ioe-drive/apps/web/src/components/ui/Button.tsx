import React from "react";
import Link from "next/link";
import { cn } from "@/utils/cn"

export type ButtonVariant =
    | "primary"
    | "secondary"
    | "ghost"
    | "outline"
    | "destructive";
export type ButtonSize = "xs" | "sm" | "md" | "lg";

export interface ButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    /** When provided, renders as a Next.js Link instead of a <button>. */
    href?: string;
    variant?: ButtonVariant;
    size?: ButtonSize;
    icon?: React.ReactNode;
    iconPosition?: "left" | "right";
    /** Compact icon-only button (children should be empty) - provide an aria-label too. */
    iconOnly?: boolean;
    className?: string;
}

const variantStyles: Record<ButtonVariant, string> = {
    primary:
        "bg-button-primary text-button-primary-text hover:bg-button-primary-hover active:bg-button-primary-active focus:ring-button-primary border border-transparent",
    secondary:
        "bg-button-secondary text-button-secondary-text border border-border hover:bg-button-secondary-hover hover:border-border-hover active:bg-button-secondary-active focus:ring-foreground",
    ghost:
        "bg-transparent text-foreground hover:bg-button-ghost-hover active:bg-background-active focus:ring-foreground border border-transparent",
    outline:
        "bg-transparent text-foreground border border-border hover:bg-foreground hover:text-foreground-inverse hover:border-foreground active:bg-button-primary-active focus:ring-foreground",
    destructive:
        "bg-error text-error-foreground border border-transparent hover:bg-error-hover active:bg-error-hover focus:ring-error",
};

const sizeStyles: Record<ButtonSize, string> = {
    xs: "text-xs px-2 py-1 gap-1 h-6",
    sm: "text-sm px-3 py-1.5 gap-1.5 h-8",
    md: "text-sm px-4 py-2 gap-2 h-10",
    lg: "text-base px-6 py-2.5 gap-2.5 h-12",
};

const base =
    "inline-flex items-center justify-center font-medium rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none cursor-pointer select-none transition-all duration-200";

const iconOnlySize: Record<ButtonSize, string> = {
    xs: "p-1.5 h-6 w-6",
    sm: "p-2 h-8 w-8",
    md: "p-2.5 h-10 w-10",
    lg: "p-3 h-12 w-12",
};

const IconWrapper = ({ children }: { children: React.ReactNode }) => (
    <span className="inline-flex items-center justify-center shrink-0">{children}</span>
);

const Button = React.forwardRef<HTMLElement, ButtonProps>(
    (
        {
            href,
            variant = "primary",
            size = "md",
            icon,
            iconPosition = "left",
            iconOnly = false,
            className,
            children,
            disabled,
            ...rest
        },
        ref
    ) => {
        const isIconOnly = iconOnly || (!children && !!icon);
        const classes = cn(
            base,
            variantStyles[variant],
            isIconOnly ? iconOnlySize[size] : sizeStyles[size],
            className
        );

        const iconElement = icon ? (
            <IconWrapper>{icon}</IconWrapper>
        ) : null;

        const content = isIconOnly ? (
            iconElement
        ) : (
            <>
                {icon && iconPosition === "left" && iconElement}
                {children && <span className="truncate">{children}</span>}
                {icon && iconPosition === "right" && iconElement}
            </>
        );

        if (href) {
            // A native `disabled` attribute (and the CSS `disabled:` variants above) has no
            // effect on an <a> - Link needs its own click/keyboard guard to actually block navigation.
            return (
                <Link
                    // eslint-disable-next-line @typescript-eslint/no-explicit-any
                    ref={ref as any}
                    href={href}
                    className={cn(classes, disabled && "opacity-50 cursor-not-allowed pointer-events-none")}
                    target={href.startsWith("http") ? "_blank" : undefined}
                    aria-disabled={disabled || undefined}
                    tabIndex={disabled ? -1 : undefined}
                    onClick={disabled ? (e) => e.preventDefault() : undefined}
                    // eslint-disable-next-line @typescript-eslint/no-explicit-any
                    {...(rest as any)}
                >
                    {content}
                </Link>
            );
        }

        return (
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            <button ref={ref as any} className={classes} disabled={disabled} {...rest}>
                {content}
            </button>
        );
    }
);

Button.displayName = "Button";

export default Button;