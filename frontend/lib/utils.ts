/**
 * Utility functions for the application
 */

import { type ClassValue, clsx } from 'clsx'

// Merge class names
export function cn(...inputs: ClassValue[]) {
    return clsx(inputs)
}

// Format date to readable string
export function formatDate(date: Date | string | null | undefined): string {
    if (!date) return 'N/A'

    try {
        const d = typeof date === 'string' ? new Date(date) : date
        if (isNaN(d.getTime())) return 'Invalid Date'

        return d.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
        })
    } catch (error) {
        return 'Invalid Date'
    }
}

// Calculate BMI
export function calculateBMI(heightCm: number, weightKg: number): number {
    const heightM = heightCm / 100
    return Number((weightKg / (heightM * heightM)).toFixed(1))
}

// Get BMI category
export function getBMICategory(bmi: number): string {
    if (bmi < 18.5) return 'Underweight'
    if (bmi < 25) return 'Normal'
    if (bmi < 30) return 'Overweight'
    return 'Obese'
}

// Get health score color
export function getHealthScoreColor(score: number): string {
    if (score >= 80) return 'text-green-600'
    if (score >= 65) return 'text-blue-600'
    if (score >= 50) return 'text-yellow-600'
    return 'text-red-600'
}

// Get health score background color
export function getHealthScoreBgColor(score: number): string {
    if (score >= 80) return 'bg-green-100'
    if (score >= 65) return 'bg-blue-100'
    if (score >= 50) return 'bg-yellow-100'
    return 'bg-red-100'
}

// Truncate text
export function truncate(text: string, length: number): string {
    if (text.length <= length) return text
    return text.substring(0, length) + '...'
}

// Generate user ID (temporary - replace with real auth)
export function generateUserId(): string {
    return `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

// Get or create user ID
export function getUserId(): string {
    if (typeof window === 'undefined') return 'demo_user'

    let userId = localStorage.getItem('ovasense_user_id')
    if (!userId) {
        userId = generateUserId()
        localStorage.setItem('ovasense_user_id', userId)
    }
    return userId
}
