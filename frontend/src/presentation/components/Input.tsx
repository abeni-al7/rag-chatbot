import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
}

export const Input: React.FC<InputProps> = ({ 
    label, 
    error, 
    className = '', 
    ...props 
}) => {
    return (
        <div className="w-full">
            {label && (
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    {label}
                </label>
            )}
            <input
                className={`
                    w-full px-4 py-2 rounded-lg border border-gray-300 
                    focus:ring-2 focus:ring-blue-500 focus:border-transparent 
                    outline-none transition-all duration-200
                    disabled:bg-gray-100 disabled:text-gray-500
                    ${error ? 'border-red-500 focus:ring-red-500' : ''}
                    ${className}
                `}
                {...props}
            />
            {error && (
                <p className="mt-1 text-sm text-red-600">{error}</p>
            )}
        </div>
    );
};
