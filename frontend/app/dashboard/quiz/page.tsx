/**
 * PCOS Awareness Quiz Page
 * Tab 6: Interactive Quiz with Scoring
 */

'use client'

import { useState, useEffect } from 'react'
import { useUser } from '@/context/UserContext'
import { quizAPI } from '@/lib/api'
import Card from '@/components/ui/Card'
import Button from '@/components/ui/Button'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import { Trophy, CheckCircle, Award } from 'lucide-react'
import toast from 'react-hot-toast'

export default function QuizPage() {
    const { userId } = useUser()
    const [questions, setQuestions] = useState<any[]>([])
    const [answers, setAnswers] = useState<Record<string, string>>({})
    const [loading, setLoading] = useState(true)
    const [submitting, setSubmitting] = useState(false)
    const [result, setResult] = useState<any>(null)
    const [currentQuestion, setCurrentQuestion] = useState(0)

    useEffect(() => {
        const fetchQuestions = async () => {
            try {
                const response = await quizAPI.getQuestions()
                // Parse options if they come as JSON string from backend
                const parsedQuestions = response.data.map((q: any) => ({
                    ...q,
                    options: typeof q.options === 'string' ? JSON.parse(q.options) : q.options
                }))
                setQuestions(parsedQuestions)
            } catch (error) {
                console.error('Quiz error:', error)
                toast.error('Failed to load quiz questions')
            } finally {
                setLoading(false)
            }
        }

        fetchQuestions()
    }, [])

    const handleAnswer = (questionId: number, answer: string) => {
        setAnswers({ ...answers, [questionId]: answer })
    }

    const handleSubmit = async () => {
        if (!userId) return

        try {
            setSubmitting(true)
            const response = await quizAPI.submitQuiz({
                user_id: userId,
                answers: answers,
            })
            setResult(response.data)
            toast.success('Quiz submitted successfully!')
        } catch (error) {
            toast.error('Failed to submit quiz')
        } finally {
            setSubmitting(false)
        }
    }

    const handleNext = () => {
        if (currentQuestion < questions.length - 1) {
            setCurrentQuestion(currentQuestion + 1)
        }
    }

    const handlePrevious = () => {
        if (currentQuestion > 0) {
            setCurrentQuestion(currentQuestion - 1)
        }
    }

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <LoadingSpinner size="lg" />
            </div>
        )
    }

    if (result) {
        return (
            <div className="space-y-8">
                <Card className="bg-gradient-to-br from-purple-50 to-pink-50 text-center">
                    <Trophy className="w-20 h-20 text-yellow-500 mx-auto mb-4" />
                    <h2 className="text-3xl font-bold text-gray-900 mb-2">Quiz Complete!</h2>
                    <div className="text-6xl font-bold text-purple-600 my-6">
                        {result.score}/{result.total_questions}
                    </div>
                    <p className="text-2xl font-semibold text-gray-800 mb-2">
                        {result.percentage}% Correct
                    </p>
                    <div className="inline-flex items-center px-6 py-3 bg-purple-600 text-white rounded-full text-lg font-medium mt-4">
                        <Award className="w-6 h-6 mr-2" />
                        {result.awareness_level} Level
                    </div>
                </Card>

                <Card>
                    <h3 className="text-xl font-bold text-gray-900 mb-4">Health Tips Unlocked</h3>
                    <div className="space-y-3">
                        {result.health_tips?.map((tip: string, index: number) => (
                            <div key={index} className="p-4 bg-green-50 rounded-lg border-l-4 border-green-500 flex items-start">
                                <CheckCircle className="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" />
                                <p className="text-gray-700">{tip}</p>
                            </div>
                        ))}
                    </div>
                </Card>

                <Button onClick={() => { setResult(null); setAnswers({}); setCurrentQuestion(0); }} className="w-full">
                    Take Quiz Again
                </Button>
            </div>
        )
    }

    if (questions.length === 0) {
        return (
            <Card>
                <p className="text-center text-gray-600">No quiz questions available. Please run the seed_quiz.py script on the backend.</p>
            </Card>
        )
    }

    const question = questions[currentQuestion]
    const progress = ((currentQuestion + 1) / questions.length) * 100
    const questionOptions = Array.isArray(question?.options) ? question.options : []

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">PCOS Awareness Quiz</h1>
                <p className="text-gray-600 mt-2">Test your knowledge about PCOS</p>
            </div>

            {/* Progress Bar */}
            <div>
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                    <span>Question {currentQuestion + 1} of {questions.length}</span>
                    <span>{Math.round(progress)}% Complete</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                        className="bg-purple-600 h-3 rounded-full transition-all duration-300"
                        style={{ width: `${progress}%` }}
                    />
                </div>
            </div>

            {/* Question Card */}
            <Card>
                <h3 className="text-xl font-bold text-gray-900 mb-6">{question.question}</h3>
                <div className="space-y-3">
                    {questionOptions.map((option: string, index: number) => (
                        <button
                            key={index}
                            onClick={() => handleAnswer(question.id, option)}
                            className={`w-full p-4 text-left rounded-lg border-2 transition-all ${answers[question.id] === option
                                ? 'border-purple-600 bg-purple-50'
                                : 'border-gray-200 hover:border-purple-300 hover:bg-gray-50'
                                }`}
                        >
                            <div className="flex items-center">
                                <div className={`w-6 h-6 rounded-full border-2 mr-3 flex items-center justify-center ${answers[question.id] === option
                                    ? 'border-purple-600 bg-purple-600'
                                    : 'border-gray-300'
                                    }`}>
                                    {answers[question.id] === option && (
                                        <CheckCircle className="w-4 h-4 text-white" />
                                    )}
                                </div>
                                <span className="text-gray-800">{option}</span>
                            </div>
                        </button>
                    ))}
                </div>
            </Card>

            {/* Navigation */}
            <div className="flex justify-between">
                <Button
                    onClick={handlePrevious}
                    disabled={currentQuestion === 0}
                    variant="outline"
                >
                    Previous
                </Button>

                {currentQuestion === questions.length - 1 ? (
                    <Button
                        onClick={handleSubmit}
                        disabled={submitting || Object.keys(answers).length < questions.length}
                    >
                        {submitting ? 'Submitting...' : 'Submit Quiz'}
                    </Button>
                ) : (
                    <Button onClick={handleNext}>
                        Next
                    </Button>
                )}
            </div>
        </div>
    )
}
