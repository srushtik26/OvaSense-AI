'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Heart, Shield, Brain, ArrowRight } from 'lucide-react'

export default function Home() {
  const router = useRouter()

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Heart className="w-8 h-8 text-purple-600" />
            <h1 className="text-2xl font-bold text-gray-800">OvaSense AI</h1>
          </div>
          <button
            onClick={() => router.push('/dashboard/home')}
            className="px-4 py-2 text-purple-600 hover:text-purple-700 font-medium"
          >
            Go to Dashboard
          </button>
        </div>
      </header>

      {/* Hero Section */}
      <main className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto text-center">
          <div className="mb-8">
            <h2 className="text-5xl font-bold text-gray-900 mb-4">
              Your Complete PCOS{' '}
              <span className="text-purple-600">Health Platform</span>
            </h2>
            <p className="text-xl text-gray-600 mb-6">
              Track, manage, and improve your PCOS journey with AI-powered insights
            </p>
            <p className="text-lg text-gray-500 max-w-2xl mx-auto">
              Comprehensive health tracking, personalized diet plans, mental health support,
              and expert guidance - all in one place.
            </p>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <div className="bg-white p-6 rounded-xl shadow-md">
              <Shield className="w-12 h-12 text-purple-600 mx-auto mb-4" />
              <h3 className="font-semibold text-lg mb-2">Safe & Private</h3>
              <p className="text-gray-600 text-sm">
                Your data is secure and private. No medical diagnosis, just insights.
              </p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-md">
              <Brain className="w-12 h-12 text-purple-600 mx-auto mb-4" />
              <h3 className="font-semibold text-lg mb-2">AI-Powered</h3>
              <p className="text-gray-600 text-sm">
                Advanced pattern detection using machine learning and medical insights.
              </p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-md">
              <Heart className="w-12 h-12 text-purple-600 mx-auto mb-4" />
              <h3 className="font-semibold text-lg mb-2">Comprehensive</h3>
              <p className="text-gray-600 text-sm">
                Period tracking, mental health, diet plans, and progress reports.
              </p>
            </div>
          </div>

          {/* CTA Button */}
          <button
            onClick={() => router.push('/dashboard/home')}
            className="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-4 px-8 rounded-lg text-lg shadow-lg transition-all duration-200 flex items-center space-x-2 mx-auto"
          >
            <span>Get Started</span>
            <ArrowRight className="w-5 h-5" />
          </button>

          {/* Disclaimer */}
          <div className="mt-12 p-6 bg-red-50 border-l-4 border-red-500 rounded-lg max-w-3xl mx-auto">
            <p className="text-sm text-red-800 font-medium">
              <strong>Important:</strong> This system does not diagnose PCOS. It detects
              patterns associated with hormonal imbalance and suggests consulting a medical
              professional for proper evaluation.
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-8 text-center text-gray-600 text-sm">
        <p>© 2024 OvaSense AI v2.0. For informational purposes only.</p>
      </footer>
    </div>
  )
}

