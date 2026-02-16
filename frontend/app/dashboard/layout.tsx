/**
 * Dashboard Layout
 * Wraps all dashboard pages with sidebar and header
 */

'use client'

import { UserProvider } from '@/context/UserContext'
import Sidebar from '@/components/layout/Sidebar'
import Header from '@/components/layout/Header'
import { Toaster } from 'react-hot-toast'

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <UserProvider>
            <div className="flex min-h-screen bg-gray-50">
                <Sidebar />
                <div className="flex-1 flex flex-col">
                    <Header />
                    <main className="flex-1 p-8">
                        {children}
                    </main>
                </div>
            </div>
            <Toaster position="top-right" />
        </UserProvider>
    )
}
