/**
 * Dashboard Home Page
 * Tab 1: Health Score + Quick Stats + Recent Activity
 */

'use client'

import { useUser } from '@/context/UserContext'
import { useHealthScore } from '@/lib/hooks/useHealthScore'
import Card from '@/components/ui/Card'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import { Activity, TrendingUp, Heart, Calendar } from 'lucide-react'
import { getHealthScoreColor, getHealthScoreBgColor } from '@/lib/utils'

export default function DashboardHome() {
    const { userId } = useUser()
    const { data: healthScore, loading, error } = useHealthScore(userId)

    return (
        <div className="space-y-8">
            {/* Page Header */}
            <div>
                <h1 className="text-3xl font-bold text-gray-900">Welcome to Your Health Dashboard</h1>
                <p className="text-gray-600 mt-2">Track your PCOS journey and stay on top of your health</p>
            </div>

            {/* Health Score Card */}
            <Card className="bg-gradient-to-br from-purple-50 to-pink-50">
                <div className="flex items-center justify-between">
                    <div>
                        <p className="text-sm font-medium text-gray-600 mb-2">Your Health Score</p>
                        {loading ? (
                            <LoadingSpinner />
                        ) : error ? (
                            <p className="text-red-600">No data available yet</p>
                        ) : healthScore ? (
                            <>
                                <div className="flex items-baseline space-x-2">
                                    <span className={`text-6xl font-bold ${getHealthScoreColor(healthScore.health_score)}`}>
                                        {healthScore.health_score}
                                    </span>
                                    <span className="text-2xl text-gray-500">/100</span>
                                </div>
                                <p className="text-lg font-medium text-gray-700 mt-2">{healthScore.status}</p>
                                <p className="text-sm text-gray-600 mt-1">{healthScore.message}</p>
                            </>
                        ) : (
                            <p className="text-gray-600">Complete an assessment to see your score</p>
                        )}
                    </div>
                    <div className="w-32 h-32 rounded-full bg-white flex items-center justify-center shadow-lg">
                        <Heart className="w-16 h-16 text-purple-600" />
                    </div>
                </div>
            </Card>

            {/* Quick Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card hover>
                    <div className="flex items-center space-x-4">
                        <div className="p-3 bg-blue-100 rounded-lg">
                            <Calendar className="w-6 h-6 text-blue-600" />
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Period Tracking</p>
                            <p className="text-2xl font-bold text-gray-900">Active</p>
                        </div>
                    </div>
                </Card>

                <Card hover>
                    <div className="flex items-center space-x-4">
                        <div className="p-3 bg-green-100 rounded-lg">
                            <Activity className="w-6 h-6 text-green-600" />
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Mental Health</p>
                            <p className="text-2xl font-bold text-gray-900">Tracked</p>
                        </div>
                    </div>
                </Card>

                <Card hover>
                    <div className="flex items-center space-x-4">
                        <div className="p-3 bg-purple-100 rounded-lg">
                            <TrendingUp className="w-6 h-6 text-purple-600" />
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Progress</p>
                            <p className="text-2xl font-bold text-gray-900">Improving</p>
                        </div>
                    </div>
                </Card>
            </div>

            {/* Health Score Breakdown */}
            {healthScore && healthScore.breakdown && (
                <Card>
                    <h3 className="text-xl font-bold text-gray-900 mb-4">Health Score Breakdown</h3>
                    <div className="space-y-4">
                        {Object.entries(healthScore.breakdown).map(([key, value]) => (
                            <div key={key}>
                                <div className="flex justify-between items-center mb-2">
                                    <span className="text-sm font-medium text-gray-700 capitalize">
                                        {key.replace(/_/g, ' ')}
                                    </span>
                                    <span className="text-sm font-bold text-gray-900">{value}/100</span>
                                </div>
                                <div className="w-full bg-gray-200 rounded-full h-2">
                                    <div
                                        className="bg-purple-600 h-2 rounded-full transition-all duration-500"
                                        style={{ width: `${value}%` }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </Card>
            )}

            {/* Quick Actions */}
            <Card>
                <h3 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <a
                        href="/dashboard/period"
                        className="p-4 border-2 border-gray-200 rounded-lg hover:border-purple-600 hover:bg-purple-50 transition-all text-center"
                    >
                        <Calendar className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                        <p className="text-sm font-medium text-gray-900">Log Period</p>
                    </a>
                    <a
                        href="/dashboard/mental-health"
                        className="p-4 border-2 border-gray-200 rounded-lg hover:border-purple-600 hover:bg-purple-50 transition-all text-center"
                    >
                        <Activity className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                        <p className="text-sm font-medium text-gray-900">Log Mood</p>
                    </a>
                    <a
                        href="/dashboard/diet"
                        className="p-4 border-2 border-gray-200 rounded-lg hover:border-purple-600 hover:bg-purple-50 transition-all text-center"
                    >
                        <Heart className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                        <p className="text-sm font-medium text-gray-900">View Diet</p>
                    </a>
                    <a
                        href="/dashboard/quiz"
                        className="p-4 border-2 border-gray-200 rounded-lg hover:border-purple-600 hover:bg-purple-50 transition-all text-center"
                    >
                        <TrendingUp className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                        <p className="text-sm font-medium text-gray-900">Take Quiz</p>
                    </a>
                </div>
            </Card>
        </div>
    )
}
