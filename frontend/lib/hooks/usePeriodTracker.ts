/**
 * Custom hook for period tracker functionality
 */

'use client'

import { useState, useEffect } from 'react'
import { periodAPI } from '../api'

export function usePeriodHistory(userId: string | null) {
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
            const response = await periodAPI.getHistory(userId)
            setData(response.data)
            setError(null)
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to fetch period history')
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

export function usePeriodPrediction(userId: string | null) {
    const [data, setData] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!userId) {
            setLoading(false)
            return
        }

        const fetchPrediction = async () => {
            try {
                setLoading(true)
                const response = await periodAPI.getPrediction(userId)
                setData(response.data)
                setError(null)
            } catch (err: any) {
                setError(err.response?.data?.detail || 'Failed to fetch prediction')
                setData(null)
            } finally {
                setLoading(false)
            }
        }

        fetchPrediction()
    }, [userId])

    return { data, loading, error }
}
