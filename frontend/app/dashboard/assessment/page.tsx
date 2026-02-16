/**
 * Assessment Page
 * Tab 2: PCOS Risk Assessment (Migrated from existing)
 */

'use client'

import { useRouter } from 'next/navigation'
import Card from '@/components/ui/Card'
import Button from '@/components/ui/Button'
import { ClipboardList, ArrowRight } from 'lucide-react'

export default function AssessmentPage() {
    const router = useRouter()

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">PCOS Risk Assessment</h1>
                <p className="text-gray-600 mt-2">Get your personalized PCOS risk analysis</p>
            </div>

            <Card className="bg-gradient-to-br from-blue-50 to-purple-50">
                <div className="flex items-center justify-between">
                    <div className="flex-1">
                        <h3 className="text-2xl font-bold text-gray-900 mb-3">Take Your Assessment</h3>
                        <p className="text-gray-700 mb-4">
                            Complete a comprehensive questionnaire to receive:
                        </p>
                        <ul className="space-y-2 mb-6">
                            <li className="flex items-center text-gray-700">
                                <span className="text-purple-600 mr-2">✓</span>
                                PCOS Risk Level (Low, Moderate, High)
                            </li>
                            <li className="flex items-center text-gray-700">
                                <span className="text-purple-600 mr-2">✓</span>
                                Phenotype Classification
                            </li>
                            <li className="flex items-center text-gray-700">
                                <span className="text-purple-600 mr-2">✓</span>
                                Personalized Remedies & Recommendations
                            </li>
                            <li className="flex items-center text-gray-700">
                                <span className="text-purple-600 mr-2">✓</span>
                                AI-Powered Insights
                            </li>
                        </ul>
                        <Button onClick={() => router.push('/assessment')} size="lg">
                            Start Assessment
                            <ArrowRight className="w-5 h-5 ml-2" />
                        </Button>
                    </div>
                    <ClipboardList className="w-32 h-32 text-purple-600 ml-8" />
                </div>
            </Card>

            {/* Info Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card hover>
                    <h4 className="font-bold text-gray-900 mb-2">Quick & Easy</h4>
                    <p className="text-sm text-gray-600">
                        Takes only 3-5 minutes to complete the questionnaire
                    </p>
                </Card>

                <Card hover>
                    <h4 className="font-bold text-gray-900 mb-2">Private & Secure</h4>
                    <p className="text-sm text-gray-600">
                        Your data is encrypted and never shared with third parties
                    </p>
                </Card>

                <Card hover>
                    <h4 className="font-bold text-gray-900 mb-2">AI-Powered</h4>
                    <p className="text-sm text-gray-600">
                        Advanced machine learning provides accurate risk assessment
                    </p>
                </Card>
            </div>

            {/* Disclaimer */}
            <Card className="border-l-4 border-red-500 bg-red-50">
                <p className="text-sm text-red-800">
                    <strong>Important:</strong> This assessment does not diagnose PCOS. It detects patterns
                    associated with hormonal imbalance and suggests consulting a medical professional for
                    proper evaluation.
                </p>
            </Card>
        </div>
    )
}
