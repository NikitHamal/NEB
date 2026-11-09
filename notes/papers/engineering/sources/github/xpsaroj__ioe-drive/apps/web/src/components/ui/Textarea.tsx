import React from 'react';
import { cn } from '@/utils/cn';

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
    label?: string;
    error?: string;
    helperText?: string;
    placeholder?: string;
}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
    ({ label, error, helperText, placeholder, className, id, rows = 4, ...props }, ref) => {
        const textareaId = id || label?.toLowerCase().replace(/\s+/g, '-');

        return (
            <div className="w-full">
                {label && (
                    <label
                        htmlFor={textareaId}
                        className="block text-sm font-medium text-foreground mb-1"
                    >
                        {label}
                        {props.required && <span className="text-error ml-1">*</span>}
                    </label>
                )}
                <textarea
                    ref={ref}
                    id={textareaId}
                    rows={rows}
                    placeholder={placeholder}
                    className={cn(
                        'w-full px-3 py-2.5 border rounded-lg transition-all resize-y',
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

Textarea.displayName = 'Textarea';

export default Textarea;
