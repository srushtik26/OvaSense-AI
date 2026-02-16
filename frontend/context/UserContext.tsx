/**
 * User Context Provider
 * Manages global user state
 */

'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { getUserId } from '@/lib/utils'

interface UserContextType {
    userId: string | null
    setUserId: (id: string) => void
}

const UserContext = createContext<UserContextType | undefined>(undefined)

export function UserProvider({ children }: { children: React.ReactNode }) {
    const [userId, setUserIdState] = useState<string | null>(null)

    useEffect(() => {
        // Get or create user ID on mount
        const id = getUserId()
        setUserIdState(id)
    }, [])

    const setUserId = (id: string) => {
        setUserIdState(id)
        if (typeof window !== 'undefined') {
            localStorage.setItem('ovasense_user_id', id)
        }
    }

    return (
        <UserContext.Provider value={{ userId, setUserId }}>
            {children}
        </UserContext.Provider>
    )
}

export function useUser() {
    const context = useContext(UserContext)
    if (context === undefined) {
        throw new Error('useUser must be used within a UserProvider')
    }
    return context
}
