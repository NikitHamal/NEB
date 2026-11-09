import React from 'react';
import clsx from 'clsx';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
    helperText?: string;
    placeholder?: string;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
    ({ label, error, helperText, placeholder, className, id, ...props }, ref) => {
        const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');

        return (
            <div className="w-full">
                {label && (
                    <label
                        htmlFor={inputId}
                        className="block text-sm font-medium text-foreground mb-1"
                    >
                        {label}
                        {props.required && <span className="text-error ml-1">*</span>}
                    </label>
                )}
                <input
                    ref={ref}
                    id={inputId}
                    placeholder={placeholder}
                    className={clsx(
                        'w-full px-3 py-2.5 border rounded-lg transition-all',
                        'focus:ring-2 focus:ring-foreground focus:border-transparent outline-none',
                        'disabled:bg-input-disabled disabled:text-foreground-tertiary disabled:cursor-not-allowed',
                        {
                            'border-error bg-error/10 focus:ring-error': error,
                            'bg-background hover:border-input-placeholder': !error,
                        },
                        className
                    )}
                    {...props}
                />
                {error && <p className="mt-1.5 text-xs text-error">{error}</p>}
                {helperText && !error && (
                    <p className="mt-1.5 text-xs text-foreground-tertiary">{helperText}</p>
                )}
            </div>
        );
    }
);

Input.displayName = 'Input';

export default Input;
