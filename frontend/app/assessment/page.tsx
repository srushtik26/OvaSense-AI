'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { ArrowLeft, ArrowRight, Loader2 } from 'lucide-react'
import axios from 'axios'

interface AssessmentForm {
  // Personal
  age: number
  height_cm: number
  weight_kg: number
  family_history_pcos: boolean

  // Menstrual
  cycle_length_avg: number
  cycles_last_12_months: number
  missed_period_frequency: number
  period_flow_type: 'light' | 'normal' | 'heavy'
  taken_birth_control_pills: boolean

  // Symptoms
  acne_severity: number
  facial_hair_growth: number
  hair_thinning: number
  dark_patches_skin: boolean

  // Metabolic
  sudden_weight_gain: boolean
  fatigue_level: number
  sugar_cravings: number

  // Lifestyle
  stress_level: number
  sleep_hours: number
  exercise_days_per_week: number
  diet_type: string
}

const STEPS = [
  { id: 1, title: 'Personal Details', fields: ['age', 'height_cm', 'weight_kg', 'family_history_pcos'] },
  { id: 2, title: 'Menstrual Health', fields: ['cycle_length_avg', 'cycles_last_12_months', 'missed_period_frequency', 'period_flow_type', 'taken_birth_control_pills'] },
  { id: 3, title: 'Symptoms', fields: ['acne_severity', 'facial_hair_growth', 'hair_thinning', 'dark_patches_skin'] },
  { id: 4, title: 'Metabolic Factors', fields: ['sudden_weight_gain', 'fatigue_level', 'sugar_cravings'] },
  { id: 5, title: 'Lifestyle', fields: ['stress_level', 'sleep_hours', 'exercise_days_per_week', 'diet_type'] },
]

export default function AssessmentPage() {
  const router = useRouter()
  const { register, handleSubmit, formState: { errors }, watch, setValue, getValues } = useForm<AssessmentForm>({
    mode: 'onChange',
    shouldUnregister: false,
    defaultValues: {
      age: undefined,
      height_cm: undefined,
      weight_kg: undefined,
      family_history_pcos: false,
      cycle_length_avg: undefined,
      cycles_last_12_months: undefined,
      missed_period_frequency: undefined,
      period_flow_type: '',
      taken_birth_control_pills: false,
      acne_severity: 0,
      facial_hair_growth: 0,
      hair_thinning: 0,
      dark_patches_skin: false,
      sudden_weight_gain: false,
      fatigue_level: 0,
      sugar_cravings: 0,
      stress_level: 0,
      sleep_hours: undefined,
      exercise_days_per_week: undefined,
      diet_type: ''
    }
  })
  const [currentStep, setCurrentStep] = useState(1)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const onSubmit = async (data: AssessmentForm) => {
    setIsSubmitting(true)
    try {
      // Get user ID from localStorage
      const userId = localStorage.getItem('ovasense_user_id') || `user_${Date.now()}`
      if (!localStorage.getItem('ovasense_user_id')) {
        localStorage.setItem('ovasense_user_id', userId)
      }

      // Ensure all required fields are present
      const submitData = {
        ...data,
        user_id: userId,
        taken_birth_control_pills: data.taken_birth_control_pills ?? false
      }

      console.log('Submitting assessment:', submitData)

      const response = await axios.post('/api/assessments/analyze', submitData)

      if (response.data && response.data.assessment_id) {
        // Store assessment completion flag
        localStorage.setItem('ovasense_assessment_completed', 'true')
        localStorage.setItem('ovasense_assessment_id', response.data.assessment_id.toString())
        localStorage.setItem('ovasense_health_score', response.data.risk_score?.toString() || '0')
        localStorage.setItem('ovasense_phenotype', response.data.phenotype || '')

        // Show success message
        alert(`✅ Assessment Complete!\n\nYour Health Score: ${response.data.risk_score}/100\nPhenotype: ${response.data.phenotype}\n\nRedirecting to your dashboard...`)

        // Redirect to dashboard home
        router.push('/dashboard/home')
      } else {
        throw new Error('Invalid response from server')
      }
    } catch (error: any) {
      console.error('Error submitting assessment:', error)

      let errorMessage = 'An error occurred. Please try again.'

      if (error.response) {
        const serverError = error.response.data
        if (serverError && serverError.detail) {
          errorMessage = `Error: ${serverError.detail}`
        } else if (serverError && typeof serverError === 'string') {
          errorMessage = `Error: ${serverError}`
        } else {
          errorMessage = `Server error: ${error.response.status} ${error.response.statusText}`
        }
      } else if (error.request) {
        errorMessage = 'Cannot connect to server. Please make sure the backend is running on port 8000.'
      } else {
        errorMessage = error.message || 'An unexpected error occurred.'
      }

      alert(errorMessage)
      setIsSubmitting(false)
    }
  }

  const nextStep = () => {
    if (currentStep < STEPS.length) {
      setCurrentStep(currentStep + 1)
    }
  }

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Personal Details</h2>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Age
              </label>
              <input
                key={`step1-age-${currentStep}`}
                type="number"
                {...register('age', {
                  required: true,
                  min: 13,
                  max: 60,
                  valueAsNumber: true
                })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-900 bg-white"
                placeholder="Enter your age"
              />
              {errors.age && <p className="text-red-500 text-sm mt-1">Please enter a valid age (13-60)</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Height (cm)
              </label>
              <input
                key={`step1-height_cm-${currentStep}`}
                type="number"
                step="0.1"
                {...register('height_cm', {
                  required: true,
                  min: 100,
                  max: 250,
                  valueAsNumber: true
                })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-900 bg-white"
                placeholder="Enter height in cm"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Weight (kg)
              </label>
              <input
                key={`step1-weight_kg-${currentStep}`}
                type="number"
                step="0.1"
                {...register('weight_kg', {
                  required: true,
                  min: 30,
                  max: 200,
                  valueAsNumber: true
                })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-900 bg-white"
                placeholder="Enter weight in kg"
              />
            </div>

            <div>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  {...register('family_history_pcos')}
                  className="w-4 h-4 text-primary-600 focus:ring-primary-500"
                />
                <span className="text-sm font-medium text-gray-700">
                  Family history of PCOS
                </span>
              </label>
            </div>
          </div>
        )

      case 2:
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Menstrual Health</h2>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Average cycle length (days)
              </label>
              <input
                key={`step2-cycle_length_avg-${currentStep}`}
                type="number"
                step="0.1"
                {...register('cycle_length_avg', {
                  required: true,
                  min: 15,
                  max: 60,
                  valueAsNumber: true
                })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-900 bg-white"
                placeholder="Enter average cycle length"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Number of cycles in last 12 months
              </label>
              <input
                key={`step2-cycles_last_12_months-${currentStep}`}
                type="number"
                {...register('cycles_last_12_months', {
                  required: true,
                  min: 0,
                  max: 12,
                  valueAsNumber: true
                })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-900 bg-white"
                placeholder="Enter number of cycles"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Number of missed periods in last year
              </label>
              <input
                key={`step2-missed_period_frequency-${currentStep}`}
                type="number"
                {...register('missed_period_frequency', {
                  required: true,
                  min: 0,
                  valueAsNumber: true
                })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-900 bg-white"
                placeholder="Enter number of missed periods"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Period flow type
              </label>
              <select
                {...register('period_flow_type', { required: true })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-900 bg-white"
              >
                <option value="">Select...</option>
                <option value="light">Light</option>
                <option value="normal">Normal</option>
                <option value="heavy">Heavy</option>
              </select>
            </div>

            <div>
              <label className="flex items-center space-x-2">
                <input
                  key={`step2-taken_birth_control_pills-${currentStep}`}
                  type="checkbox"
                  {...register('taken_birth_control_pills')}
                  className="w-4 h-4 text-primary-600 focus:ring-primary-500"
                />
                <span className="text-sm font-medium text-gray-700">
                  Have you taken birth control pills (oral contraceptives) in the past?
                </span>
              </label>
              <p className="text-xs text-gray-500 mt-1 ml-6">
                This helps identify if symptoms might be related to post-pill hormonal changes
              </p>
            </div>
          </div>
        )

      case 3:
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Symptoms</h2>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Acne severity (0-5)
              </label>
              <input
                type="range"
                min="0"
                max="5"
                {...register('acne_severity', { required: true, valueAsNumber: true })}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>None (0)</span>
                <span>Severe (5)</span>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Facial hair growth (0-5)
              </label>
              <input
                type="range"
                min="0"
                max="5"
                {...register('facial_hair_growth', { required: true, valueAsNumber: true })}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>None (0)</span>
                <span>Severe (5)</span>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Hair thinning (0-5)
              </label>
              <input
                type="range"
                min="0"
                max="5"
                {...register('hair_thinning', { required: true, valueAsNumber: true })}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>None (0)</span>
                <span>Severe (5)</span>
              </div>
            </div>

            <div>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  {...register('dark_patches_skin')}
                  className="w-4 h-4 text-primary-600 focus:ring-primary-500"
                />
                <span className="text-sm font-medium text-gray-700">
                  Dark patches on skin (acanthosis nigricans)
                </span>
              </label>
            </div>
          </div>
        )

      case 4:
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Metabolic Factors</h2>

            <div>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  {...register('sudden_weight_gain')}
                  className="w-4 h-4 text-primary-600 focus:ring-primary-500"
                />
                <span className="text-sm font-medium text-gray-700">
                  Sudden weight gain
                </span>
              </label>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Fatigue level (0-5)
              </label>
              <input
                type="range"
                min="0"
                max="5"
                {...register('fatigue_level', { required: true, valueAsNumber: true })}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>None (0)</span>
                <span>Severe (5)</span>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Sugar cravings (0-5)
              </label>
              <input
                type="range"
                min="0"
                max="5"
                {...register('sugar_cravings', { required: true, valueAsNumber: true })}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>None (0)</span>
                <span>Severe (5)</span>
              </div>
            </div>
          </div>
        )

      case 5:
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Lifestyle</h2>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Stress level (0-10)
              </label>
              <input
                type="range"
                min="0"
                max="10"
                {...register('stress_level', { required: true, valueAsNumber: true })}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>Low (0)</span>
                <span>High (10)</span>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Average sleep hours per day
              </label>
              <input
                type="number"
                step="0.5"
                {...register('sleep_hours', { required: true, min: 0, max: 24 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Exercise days per week
              </label>
              <input
                type="number"
                {...register('exercise_days_per_week', {
                  required: true,
                  min: 0,
                  max: 7,
                  valueAsNumber: true
                })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-900 bg-white"
                placeholder="Enter exercise days"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Diet type
              </label>
              <select
                {...register('diet_type', { required: true })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-900 bg-white"
              >
                <option value="">Select...</option>
                <option value="vegetarian">Vegetarian</option>
                <option value="non-vegetarian">Non-Vegetarian</option>
                <option value="vegan">Vegan</option>
                <option value="pescatarian">Pescatarian</option>
                <option value="other">Other</option>
              </select>
            </div>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-12">
      <div className="container mx-auto px-4 max-w-3xl">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">
              Step {currentStep} of {STEPS.length}
            </span>
            <span className="text-sm font-medium text-gray-700">
              {Math.round((currentStep / STEPS.length) * 100)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${(currentStep / STEPS.length) * 100}%` }}
            />
          </div>
        </div>

        {/* Form Card */}
        <form onSubmit={handleSubmit(onSubmit)} className="bg-white rounded-xl shadow-lg p-8">
          {/* Info message about saved answers */}
          {currentStep > 1 && (
            <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-xs text-green-700">
                ✓ Your previous answers are saved. You can go back to edit them anytime.
              </p>
            </div>
          )}

          {renderStepContent()}

          {/* Navigation Buttons */}
          <div className="flex justify-between mt-8">
            <button
              type="button"
              onClick={prevStep}
              disabled={currentStep === 1}
              className="flex items-center space-x-2 px-6 py-2 bg-gray-100 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-200 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Previous</span>
            </button>

            {currentStep < STEPS.length ? (
              <button
                type="button"
                onClick={nextStep}
                className="flex items-center space-x-2 px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
              >
                <span>Next</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                type="submit"
                disabled={isSubmitting}
                className="flex items-center space-x-2 px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Processing...</span>
                  </>
                ) : (
                  <>
                    <span>Submit Assessment</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            )}
          </div>
        </form>

        {/* Disclaimer */}
        <div className="mt-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
          <p className="text-sm text-red-800">
            <strong>Note:</strong> This assessment is for informational purposes only and
            does not constitute a medical diagnosis. Please consult a healthcare professional
            for proper evaluation.
          </p>
        </div>
      </div>
    </div>
  )
}

