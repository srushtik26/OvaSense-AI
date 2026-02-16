/**
 * Reusable Button Component
 */

import { ButtonHTMLAttributes, forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
    size?: 'sm' | 'md' | 'lg'
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, variant = 'primary', size = 'md', ...props }, ref) => {
        const baseStyles = 'inline-flex items-center justify-center rounded-lg font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed'

        const variants = {
            primary: 'bg-purple-600 text-white hover:bg-purple-700 shadow-md hover:shadow-lg',
            secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
            outline: 'border-2 border-purple-600 text-purple-600 hover:bg-purple-50',
            ghost: 'text-gray-700 hover:bg-gray-100',
            danger: 'bg-red-600 text-white hover:bg-red-700',
        }

        const sizes = {
            sm: 'px-3 py-1.5 text-sm',
            md: 'px-4 py-2 text-base',
            lg: 'px-6 py-3 text-lg',
        }

        return (
            <button
                ref={ref}
                className={cn(baseStyles, variants[variant], sizes[size], className)}
                {...props}
            />
        )
    }
)

Button.displayName = 'Button'

export default Button
