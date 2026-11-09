import React from 'react';
import clsx from 'clsx';

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
    label?: string;
    error?: string;
    helperText?: string;
    placeholder?: string;
    options: Array<{ value: string; label: string }>;
}

const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
    ({ label, error, helperText, placeholder, options, className, id, ...props }, ref) => {
        const selectId = id || label?.toLowerCase().replace(/\s+/g, '-');

        return (
            <div className="w-full">
                {label && (
                    <label
                        htmlFor={selectId}
                        className="block text-sm font-medium text-foreground mb-1"
                    >
                        {label}
                        {props.required && <span className="text-error ml-1">*</span>}
                    </label>
                )}
                <select
                    ref={ref}
                    id={selectId}
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
                >
                    {placeholder && (
                        <option className="text-foreground-secondary" value="" disabled>
                            {placeholder}
                        </option>
                    )}
                    {options.map((option) => (
                        <option key={option.value} value={option.value}>
                            {option.label}
                        </option>
                    ))}
                </select>
                {error && <p className="mt-1.5 text-xs text-error">{error}</p>}
                {helperText && !error && (
                    <p className="mt-1.5 text-xs text-foreground-tertiary">{helperText}</p>
                )}
            </div>
        );
    }
);

Select.displayName = 'Select';

export default Select;