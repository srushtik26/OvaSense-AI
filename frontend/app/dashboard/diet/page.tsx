/**
 * Diet Plan Page
 * Tab 5: Personalized PCOS Diet Recommendations
 */

'use client'

import { useUser } from '@/context/UserContext'
import { useState, useEffect } from 'react'
import { dietAPI } from '@/lib/api'
import Card from '@/components/ui/Card'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import { Utensils, CheckCircle, XCircle, Lightbulb } from 'lucide-react'

export default function DietPlanPage() {
    const { userId } = useUser()
    const [dietPlan, setDietPlan] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    const [selectedDay, setSelectedDay] = useState('Monday')

    useEffect(() => {
        if (!userId) return

        const fetchDietPlan = async () => {
            try {
                const response = await dietAPI.getPlan(userId)
                setDietPlan(response.data)
            } catch (error) {
                console.error('Failed to fetch diet plan')
            } finally {
                setLoading(false)
            }
        }

        fetchDietPlan()
    }, [userId])

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <LoadingSpinner size="lg" />
            </div>
        )
    }

    if (!dietPlan) {
        return (
            <Card>
                <p className="text-center text-gray-600">Complete an assessment to get your personalized diet plan</p>
            </Card>
        )
    }

    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">Your Personalized Diet Plan</h1>
                <p className="text-gray-600 mt-2">PCOS-friendly nutrition recommendations</p>
            </div>

            {/* Phenotype Info */}
            <Card className="bg-gradient-to-br from-green-50 to-blue-50">
                <div className="flex items-center justify-between">
                    <div>
                        <p className="text-sm text-gray-600 mb-1">Your PCOS Type</p>
                        <h3 className="text-2xl font-bold text-gray-900">{dietPlan.phenotype}</h3>
                        <p className="text-sm text-gray-600 mt-1">BMI Category: {dietPlan.bmi_category}</p>
                    </div>
                    <Utensils className="w-16 h-16 text-green-600" />
                </div>
            </Card>

            {/* Foods to Eat & Avoid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <Card>
                    <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                        <CheckCircle className="w-6 h-6 mr-2 text-green-600" />
                        Foods to Eat
                    </h3>
                    <ul className="space-y-2">
                        {dietPlan.foods_to_eat?.map((food: string, index: number) => (
                            <li key={index} className="flex items-start">
                                <span className="text-green-600 mr-2">✓</span>
                                <span className="text-gray-700">{food}</span>
                            </li>
                        ))}
                    </ul>
                </Card>

                <Card>
                    <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                        <XCircle className="w-6 h-6 mr-2 text-red-600" />
                        Foods to Avoid
                    </h3>
                    <ul className="space-y-2">
                        {dietPlan.foods_to_avoid?.map((food: string, index: number) => (
                            <li key={index} className="flex items-start">
                                <span className="text-red-600 mr-2">✗</span>
                                <span className="text-gray-700">{food}</span>
                            </li>
                        ))}
                    </ul>
                </Card>
            </div>

            {/* Weekly Meal Plan */}
            <Card>
                <h3 className="text-xl font-bold text-gray-900 mb-4">Weekly Meal Plan</h3>

                {/* Day Selector */}
                <div className="flex space-x-2 mb-6 overflow-x-auto pb-2">
                    {days.map((day) => (
                        <button
                            key={day}
                            onClick={() => setSelectedDay(day)}
                            className={`px-4 py-2 rounded-lg font-medium transition-all whitespace-nowrap ${selectedDay === day
                                    ? 'bg-purple-600 text-white'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                }`}
                        >
                            {day}
                        </button>
                    ))}
                </div>

                {/* Meals for Selected Day */}
                {dietPlan.weekly_meal_plan?.[selectedDay] && (
                    <div className="space-y-3">
                        {dietPlan.weekly_meal_plan[selectedDay].map((meal: string, index: number) => (
                            <div key={index} className="p-4 bg-green-50 rounded-lg border-l-4 border-green-500">
                                <p className="text-gray-800">{meal}</p>
                            </div>
                        ))}
                    </div>
                )}
            </Card>

            {/* Nutritional Tips */}
            <Card>
                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                    <Lightbulb className="w-6 h-6 mr-2 text-yellow-500" />
                    Nutritional Tips
                </h3>
                <div className="space-y-3">
                    {dietPlan.nutritional_tips?.map((tip: string, index: number) => (
                        <div key={index} className="p-3 bg-yellow-50 rounded-lg border-l-4 border-yellow-400">
                            <p className="text-gray-700">💡 {tip}</p>
                        </div>
                    ))}
                </div>
            </Card>
        </div>
    )
}
