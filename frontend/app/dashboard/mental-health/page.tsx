/**
 * Mental Health Tracker Page
 * Tab 4: Daily Log Form + Charts + AI Insights
 */

'use client'

import { useState } from 'react'
import { useUser } from '@/context/UserContext'
import { useMentalHealthHistory, useMentalHealthInsights } from '@/lib/hooks/useMentalHealth'
import { mentalHealthAPI } from '@/lib/api'
import Card from '@/components/ui/Card'
import Button from '@/components/ui/Button'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import { Brain, Lightbulb, TrendingUp } from 'lucide-react'
import toast from 'react-hot-toast'

export default function MentalHealthPage() {
    const { userId } = useUser()
    const { data: history, loading, refetch } = useMentalHealthHistory(userId)
    const { data: insights } = useMentalHealthInsights(userId)

    const [formData, setFormData] = useState({
        stress_level: 5,
        mood_type: 'neutral',
        sleep_hours: 7,
        energy_level: 5,
    })
    const [submitting, setSubmitting] = useState(false)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!userId) return

        try {
            setSubmitting(true)
            await mentalHealthAPI.addLog({ ...formData, user_id: userId })
            toast.success('Mental health log added!')
            refetch()
        } catch (error) {
            toast.error('Failed to add log')
        } finally {
            setSubmitting(false)
        }
    }

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">Mental Health Tracker</h1>
                <p className="text-gray-600 mt-2">Track your mood, stress, and sleep patterns</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Daily Log Form */}
                <Card>
                    <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                        <Brain className="w-6 h-6 mr-2 text-purple-600" />
                        Daily Check-In
                    </h3>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Stress Level: {formData.stress_level}/10
                            </label>
                            <input
                                type="range"
                                min="1"
                                max="10"
                                value={formData.stress_level}
                                onChange={(e) => setFormData({ ...formData, stress_level: parseInt(e.target.value) })}
                                className="w-full"
                            />
                            <div className="flex justify-between text-xs text-gray-500 mt-1">
                                <span>Low</span>
                                <span>High</span>
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Mood
                            </label>
                            <select
                                value={formData.mood_type}
                                onChange={(e) => setFormData({ ...formData, mood_type: e.target.value })}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent text-gray-900 bg-white"
                            >
                                <option value="happy">😊 Happy</option>
                                <option value="neutral">😐 Neutral</option>
                                <option value="sad">😢 Sad</option>
                                <option value="anxious">😰 Anxious</option>
                                <option value="irritable">😠 Irritable</option>
                                <option value="energetic">⚡ Energetic</option>
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Sleep Hours: {formData.sleep_hours}h
                            </label>
                            <input
                                type="range"
                                min="0"
                                max="12"
                                step="0.5"
                                value={formData.sleep_hours}
                                onChange={(e) => setFormData({ ...formData, sleep_hours: parseFloat(e.target.value) })}
                                className="w-full"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Energy Level: {formData.energy_level}/10
                            </label>
                            <input
                                type="range"
                                min="1"
                                max="10"
                                value={formData.energy_level}
                                onChange={(e) => setFormData({ ...formData, energy_level: parseInt(e.target.value) })}
                                className="w-full"
                            />
                        </div>

                        <Button type="submit" disabled={submitting} className="w-full">
                            {submitting ? 'Saving...' : 'Save Daily Log'}
                        </Button>
                    </form>
                </Card>

                {/* Statistics */}
                <div className="space-y-6">
                    {history && (
                        <Card className="bg-gradient-to-br from-blue-50 to-purple-50">
                            <h3 className="text-xl font-bold text-gray-900 mb-4">Your Averages</h3>
                            <div className="space-y-4">
                                <div>
                                    <div className="flex justify-between mb-2">
                                        <span className="text-gray-700">Average Stress</span>
                                        <span className="font-bold text-gray-900">{history.average_stress?.toFixed(1)}/10</span>
                                    </div>
                                    <div className="w-full bg-white rounded-full h-2">
                                        <div
                                            className="bg-red-500 h-2 rounded-full"
                                            style={{ width: `${(history.average_stress / 10) * 100}%` }}
                                        />
                                    </div>
                                </div>
                                <div>
                                    <div className="flex justify-between mb-2">
                                        <span className="text-gray-700">Average Sleep</span>
                                        <span className="font-bold text-gray-900">{history.average_sleep?.toFixed(1)}h</span>
                                    </div>
                                    <div className="w-full bg-white rounded-full h-2">
                                        <div
                                            className="bg-blue-500 h-2 rounded-full"
                                            style={{ width: `${(history.average_sleep / 12) * 100}%` }}
                                        />
                                    </div>
                                </div>
                                <div>
                                    <div className="flex justify-between mb-2">
                                        <span className="text-gray-700">Average Energy</span>
                                        <span className="font-bold text-gray-900">{history.average_energy?.toFixed(1)}/10</span>
                                    </div>
                                    <div className="w-full bg-white rounded-full h-2">
                                        <div
                                            className="bg-green-500 h-2 rounded-full"
                                            style={{ width: `${(history.average_energy / 10) * 100}%` }}
                                        />
                                    </div>
                                </div>
                            </div>
                        </Card>
                    )}

                    {/* AI Insights */}
                    {insights && (
                        <Card>
                            <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                                <Lightbulb className="w-5 h-5 mr-2 text-yellow-500" />
                                AI Insights
                            </h3>
                            <div className="space-y-3">
                                {insights.insights?.map((insight: string, index: number) => (
                                    <div key={index} className="p-3 bg-yellow-50 rounded-lg border-l-4 border-yellow-400">
                                        <p className="text-sm text-gray-700">{insight}</p>
                                    </div>
                                ))}
                                {insights.recommendations?.map((rec: string, index: number) => (
                                    <div key={index} className="p-3 bg-green-50 rounded-lg border-l-4 border-green-400">
                                        <p className="text-sm text-gray-700">💡 {rec}</p>
                                    </div>
                                ))}
                            </div>
                        </Card>
                    )}
                </div>
            </div>

            {/* Recent Logs */}
            <Card>
                <h3 className="text-xl font-bold text-gray-900 mb-4">Recent Logs</h3>
                {loading ? (
                    <LoadingSpinner />
                ) : history && history.logs && history.logs.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {history.logs.slice(0, 6).map((log: any) => (
                            <div key={log.id} className="p-4 bg-gray-50 rounded-lg">
                                <p className="text-xs text-gray-500 mb-2">
                                    {new Date(log.created_at).toLocaleDateString()}
                                </p>
                                <div className="space-y-1 text-sm">
                                    <p>Stress: <span className="font-medium">{log.stress_level}/10</span></p>
                                    <p>Mood: <span className="font-medium">{log.mood_type}</span></p>
                                    <p>Sleep: <span className="font-medium">{log.sleep_hours}h</span></p>
                                    <p>Energy: <span className="font-medium">{log.energy_level}/10</span></p>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p className="text-gray-600 text-center py-8">No logs yet. Start tracking your mental health above!</p>
                )}
            </Card>
        </div>
    )
}
