/**
 * Period Tracker Page
 * Tab 3: Calendar + Log Form + Predictions
 */

'use client'

import { useState } from 'react'
import { useUser } from '@/context/UserContext'
import { usePeriodHistory, usePeriodPrediction } from '@/lib/hooks/usePeriodTracker'
import { periodAPI } from '@/lib/api'
import Card from '@/components/ui/Card'
import Button from '@/components/ui/Button'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import { Calendar, TrendingUp } from 'lucide-react'
import toast from 'react-hot-toast'
import { formatDate } from '@/lib/utils'

export default function PeriodTrackerPage() {
    const { userId } = useUser()
    const { data: history, loading, refetch } = usePeriodHistory(userId)
    const { data: prediction } = usePeriodPrediction(userId)

    const [formData, setFormData] = useState({
        start_date: '',
        end_date: '',
        flow_type: 'normal',
        pain_level: 5,
        mood: 'normal',
    })
    const [submitting, setSubmitting] = useState(false)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!userId) return

        try {
            setSubmitting(true)
            await periodAPI.addLog({ ...formData, user_id: userId })
            toast.success('Period log added successfully!')
            setFormData({
                start_date: '',
                end_date: '',
                flow_type: 'normal',
                pain_level: 5,
                mood: 'normal',
            })
            refetch()
        } catch (error) {
            toast.error('Failed to add period log')
        } finally {
            setSubmitting(false)
        }
    }

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">Period Tracker</h1>
                <p className="text-gray-600 mt-2">Track your menstrual cycle and get predictions</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Log Form */}
                <Card>
                    <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                        <Calendar className="w-6 h-6 mr-2 text-purple-600" />
                        Log Period
                    </h3>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Start Date
                            </label>
                            <input
                                type="date"
                                required
                                value={formData.start_date}
                                onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent text-gray-900 bg-white"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                End Date
                            </label>
                            <input
                                type="date"
                                required
                                value={formData.end_date}
                                onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent text-gray-900 bg-white"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Flow Type
                            </label>
                            <select
                                value={formData.flow_type}
                                onChange={(e) => setFormData({ ...formData, flow_type: e.target.value })}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent text-gray-900 bg-white"
                            >
                                <option value="light">Light</option>
                                <option value="normal">Normal</option>
                                <option value="heavy">Heavy</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Pain Level: {formData.pain_level}
                            </label>
                            <input
                                type="range"
                                min="1"
                                max="10"
                                value={formData.pain_level}
                                onChange={(e) => setFormData({ ...formData, pain_level: parseInt(e.target.value) })}
                                className="w-full"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Mood
                            </label>
                            <input
                                type="text"
                                value={formData.mood}
                                onChange={(e) => setFormData({ ...formData, mood: e.target.value })}
                                placeholder="e.g., happy, irritable, anxious"
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent text-gray-900 bg-white placeholder:text-gray-400"
                            />
                        </div>
                        <Button type="submit" disabled={submitting} className="w-full">
                            {submitting ? 'Adding...' : 'Add Period Log'}
                        </Button>
                    </form>
                </Card>

                {/* Prediction Card */}
                <div className="space-y-6">
                    <Card className="bg-gradient-to-br from-pink-50 to-purple-50">
                        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                            <TrendingUp className="w-6 h-6 mr-2 text-purple-600" />
                            Next Period Prediction
                        </h3>
                        {prediction ? (
                            <div>
                                <p className="text-4xl font-bold text-purple-600 mb-2">
                                    {formatDate(prediction.next_period_date)}
                                </p>
                                <p className="text-lg text-gray-700 mb-2">
                                    Confidence: <span className="font-semibold">{prediction.confidence}</span>
                                </p>
                                <p className="text-sm text-gray-600">{prediction.message}</p>
                            </div>
                        ) : (
                            <p className="text-gray-600">Log at least 2 periods to see predictions</p>
                        )}
                    </Card>

                    {/* Cycle Stats */}
                    {history && (
                        <Card>
                            <h3 className="text-lg font-bold text-gray-900 mb-4">Cycle Statistics</h3>
                            <div className="space-y-3">
                                <div className="flex justify-between">
                                    <span className="text-gray-600">Average Cycle Length</span>
                                    <span className="font-bold text-gray-900">{history.average_cycle_length?.toFixed(1)} days</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-gray-600">Cycle Stability</span>
                                    <span className="font-bold text-gray-900">{history.cycle_stability_score}/100</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-gray-600">Total Logs</span>
                                    <span className="font-bold text-gray-900">{history.logs?.length || 0}</span>
                                </div>
                            </div>
                        </Card>
                    )}
                </div>
            </div>

            {/* Period History */}
            <Card>
                <h3 className="text-xl font-bold text-gray-900 mb-4">Period History</h3>
                {loading ? (
                    <LoadingSpinner />
                ) : history && history.logs && history.logs.length > 0 ? (
                    <div className="space-y-3">
                        {history.logs.map((log: any) => (
                            <div key={log.id} className="p-4 bg-gray-50 rounded-lg flex justify-between items-center">
                                <div>
                                    <p className="font-medium text-gray-900">
                                        {formatDate(log.start_date)} - {formatDate(log.end_date)}
                                    </p>
                                    <p className="text-sm text-gray-600">
                                        Flow: {log.flow_type} | Pain: {log.pain_level}/10 | Mood: {log.mood}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p className="text-gray-600 text-center py-8">No period logs yet. Add your first log above!</p>
                )}
            </Card>
        </div>
    )
}
