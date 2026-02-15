'use client'

import { useState, useEffect } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import axios from 'axios'
import { Download, ArrowLeft, CheckCircle, AlertCircle, Info } from 'lucide-react'

interface AssessmentResult {
  risk_level: string
  phenotype: string
  confidence?: string
  confidence_score?: number
  risk_score: number
  key_drivers: string[]
  remedies: string[]
  next_steps: string[]
  disclaimer: string
  assessment_id?: number
}

export default function ResultsPage() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const [result, setResult] = useState<AssessmentResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [downloading, setDownloading] = useState(false)

  useEffect(() => {
    const assessmentId = searchParams.get('id')
    if (assessmentId) {
      fetchResult(parseInt(assessmentId))
    }
  }, [searchParams])

  const fetchResult = async (id: number) => {
    try {
      const response = await axios.get(`/api/assessments/${id}`)
      setResult(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching results:', error)
      setLoading(false)
    }
  }

  const downloadReport = async () => {
    if (!result?.assessment_id) return
    
    setDownloading(true)
    try {
      const response = await axios.get(
        `/api/assessments/${result.assessment_id}/report`,
        { responseType: 'blob' }
      )
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `ovasense_report_${result.assessment_id}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (error) {
      console.error('Error downloading report:', error)
      alert('Error downloading report. Please try again.')
    } finally {
      setDownloading(false)
    }
  }

  const getRiskColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-300'
      case 'moderate':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300'
      case 'low':
        return 'bg-green-100 text-green-800 border-green-300'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your results...</p>
        </div>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 mb-4">No results found.</p>
          <button
            onClick={() => router.push('/')}
            className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            Go Home
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-12">
      <div className="container mx-auto px-4 max-w-4xl">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => router.push('/')}
            className="flex items-center space-x-2 text-gray-600 hover:text-gray-800 mb-4"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Home</span>
          </button>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Your Assessment Results</h1>
          <p className="text-gray-600">Review your personalized risk assessment and recommendations</p>
        </div>

        {/* Risk Level Card */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-800">Risk Assessment</h2>
            <button
              onClick={downloadReport}
              disabled={downloading}
              className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
            >
              <Download className="w-4 h-4" />
              <span>{downloading ? 'Downloading...' : 'Download Report'}</span>
            </button>
          </div>

          <div className={`inline-block px-6 py-3 rounded-lg border-2 ${getRiskColor(result.risk_level)} mb-4`}>
            <div className="flex items-center space-x-2">
              {result.risk_level === 'High' && <AlertCircle className="w-5 h-5" />}
              {result.risk_level === 'Moderate' && <Info className="w-5 h-5" />}
              {result.risk_level === 'Low' && <CheckCircle className="w-5 h-5" />}
              <span className="text-xl font-bold">{result.risk_level} Risk</span>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-4 mb-6">
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Risk Score</p>
              <p className="text-2xl font-bold text-gray-900">{result.risk_score.toFixed(1)}%</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Confidence</p>
              <p className="text-2xl font-bold text-gray-900">
                {result.confidence || 
                 (result.confidence_score !== undefined ? `${(result.confidence_score * 100).toFixed(0)}%` : 'N/A')}
              </p>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Pattern Type</p>
              <p className="text-lg font-semibold text-gray-900">{result.phenotype}</p>
            </div>
          </div>
        </div>

        {/* Key Drivers */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Key Contributing Factors</h2>
          <ul className="space-y-2">
            {result.key_drivers.map((driver, index) => (
              <li key={index} className="flex items-start space-x-2">
                <span className="text-primary-600 mt-1">•</span>
                <span className="text-gray-700">{driver}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Lifestyle Recommendations */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Lifestyle Recommendations</h2>
          <p className="text-gray-600 mb-4">
            Based on your <strong>{result.phenotype}</strong> pattern, here are personalized recommendations:
          </p>
          <ul className="space-y-3">
            {result.remedies.map((remedy, index) => (
              <li key={index} className="flex items-start space-x-3">
                <CheckCircle className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                <span className="text-gray-700">{remedy}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Clinical Next Steps */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Suggested Clinical Next Steps</h2>
          <ul className="space-y-3">
            {result.next_steps.map((step, index) => (
              <li key={index} className="flex items-start space-x-3">
                <Info className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                <span className="text-gray-700">{step}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Important Disclaimer */}
        <div className="bg-red-50 border-l-4 border-red-500 rounded-lg p-6">
          <div className="flex items-start space-x-3">
            <AlertCircle className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-bold text-red-900 mb-2">Important Disclaimer</h3>
              <p className="text-red-800 text-sm leading-relaxed">
                {result.disclaimer || "This is not a medical diagnosis. Please consult a doctor for confirmation."}
              </p>
              <p className="text-red-800 text-sm mt-2 leading-relaxed">
                This system does not diagnose PCOS. It detects patterns associated with hormonal imbalance 
                and suggests consulting a medical professional for proper evaluation and diagnosis.
              </p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-8 flex justify-center space-x-4">
          <button
            onClick={() => router.push('/assessment')}
            className="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300"
          >
            Take Another Assessment
          </button>
          <button
            onClick={downloadReport}
            disabled={downloading}
            className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 flex items-center space-x-2"
          >
            <Download className="w-5 h-5" />
            <span>Download Full Report</span>
          </button>
        </div>
      </div>
    </div>
  )
}

