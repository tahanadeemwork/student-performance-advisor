import { GraduationCap } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-slate-900 text-slate-400 py-8 mt-16">
      <div className="max-w-7xl mx-auto px-6 text-center">
        <div className="flex items-center justify-center gap-2 mb-3">
          <GraduationCap size={20} className="text-blue-400" />
          <span className="text-white font-semibold">
            Student Performance Prediction Advisor
          </span>
        </div>
        <p className="text-sm mb-2">
          Rule-Based Expert System | Forward Chaining | Certainty Factors
        </p>
        <p className="text-xs text-slate-500">
          BS Computer Science · 4th Semester · AI Course Term Project
        </p>
        <div className="mt-4 pt-4 border-t border-slate-800 text-xs text-slate-600">
          ⚠️ For academic advisory purposes only.
          Always consult a qualified academic advisor.
        </div>
      </div>
    </footer>
  )
}