/**
 * Custom hook for mental health functionality
 */

'use client'

import { useState, useEffect } from 'react'
import { mentalHealthAPI } from '../api'

export function useMentalHealthHistory(userId: string | null) {
    const [data, setData] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    const fetchHistory = async () => {
        if (!userId) {
            setLoading(false)
            return
        }

        try {
            setLoading(true)
            const response = await mentalHealthAPI.getHistory(userId)
            setData(response.data)
            setError(null)
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to fetch mental health history')
            setData(null)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchHistory()
    }, [userId])

    return { data, loading, error, refetch: fetchHistory }
}

export function useMentalHealthInsights(userId: string | null) {
    const [data, setData] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!userId) {
            setLoading(false)
            return
        }

        const fetchInsights = async () => {
            try {
                setLoading(true)
                const response = await mentalHealthAPI.getInsights(userId)
                setData(response.data)
                setError(null)
            } catch (err: any) {
                setError(err.response?.data?.detail || 'Failed to fetch insights')
                setData(null)
            } finally {
                setLoading(false)
            }
        }

        fetchInsights()
    }, [userId])

    return { data, loading, error }
}
