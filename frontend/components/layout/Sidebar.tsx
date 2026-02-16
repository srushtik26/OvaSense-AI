/**
 * Dashboard Sidebar Navigation
 */

'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
    Home,
    ClipboardList,
    Calendar,
    Brain,
    Utensils,
    Trophy,
    FileText,
    Heart
} from 'lucide-react'
import { cn } from '@/lib/utils'

const navItems = [
    { name: 'Home', href: '/dashboard/home', icon: Home },
    { name: 'Assessment', href: '/dashboard/assessment', icon: ClipboardList },
    { name: 'Period Tracker', href: '/dashboard/period', icon: Calendar },
    { name: 'Mental Health', href: '/dashboard/mental-health', icon: Brain },
    { name: 'Diet Plan', href: '/dashboard/diet', icon: Utensils },
    { name: 'Quiz', href: '/dashboard/quiz', icon: Trophy },
    { name: 'Reports', href: '/dashboard/reports', icon: FileText },
]

export default function Sidebar() {
    const pathname = usePathname()

    return (
        <aside className="w-64 bg-white border-r border-gray-200 min-h-screen p-6">
            {/* Logo */}
            <div className="flex items-center space-x-2 mb-8">
                <Heart className="w-8 h-8 text-purple-600" />
                <h1 className="text-xl font-bold text-gray-900">OvaSense AI</h1>
            </div>

            {/* Navigation */}
            <nav className="space-y-2">
                {navItems.map((item) => {
                    const isActive = pathname === item.href
                    const Icon = item.icon

                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                'flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200',
                                isActive
                                    ? 'bg-purple-100 text-purple-700 font-medium'
                                    : 'text-gray-700 hover:bg-gray-100'
                            )}
                        >
                            <Icon className="w-5 h-5" />
                            <span>{item.name}</span>
                        </Link>
                    )
                })}
            </nav>

            {/* Footer */}
            <div className="mt-auto pt-8">
                <p className="text-xs text-gray-500 text-center">
                    OvaSense AI v2.0
                </p>
            </div>
        </aside>
    )
}
