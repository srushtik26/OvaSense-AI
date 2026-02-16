/**
 * Custom hook for fetching health score
 */

'use client'

import { useState, useEffect } from 'react'
import { healthScoreAPI } from '../api'

interface HealthScore {
    health_score: number
    status: string
    message: string
    breakdown: {
        cycle_regularity: number
        bmi: number
        stress: number
        sleep: number
        exercise: number
        symptoms: number
    }
}

export function useHealthScore(userId: string | null) {
    const [data, setData] = useState<HealthScore | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!userId) {
            setLoading(false)
            return
        }

        const fetchHealthScore = async () => {
            try {
                setLoading(true)
                const response = await healthScoreAPI.getScore(userId)
                setData(response.data)
                setError(null)
            } catch (err: any) {
                setError(err.response?.data?.detail || 'Failed to fetch health score')
                setData(null)
            } finally {
                setLoading(false)
            }
        }

        fetchHealthScore()
    }, [userId])

    return { data, loading, error }
}
