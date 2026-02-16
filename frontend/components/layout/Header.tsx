/**
 * Dashboard Header Component
 */

'use client'

import { useUser } from '@/context/UserContext'
import { Bell, User } from 'lucide-react'

export default function Header() {
    const { userId } = useUser()

    return (
        <header className="bg-white border-b border-gray-200 px-8 py-4">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-gray-900">Dashboard</h2>
                    <p className="text-sm text-gray-600">Welcome back to your health journey</p>
                </div>

                <div className="flex items-center space-x-4">
                    {/* Notifications */}
                    <button className="p-2 rounded-lg hover:bg-gray-100 transition-colors relative">
                        <Bell className="w-5 h-5 text-gray-700" />
                        <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
                    </button>

                    {/* User Profile */}
                    <div className="flex items-center space-x-3 px-4 py-2 rounded-lg bg-gray-100">
                        <div className="w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center">
                            <User className="w-5 h-5 text-white" />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-900">User</p>
                            <p className="text-xs text-gray-600">{userId?.substring(0, 12)}...</p>
                        </div>
                    </div>
                </div>
            </div>
        </header>
    )
}
