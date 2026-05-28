import { motion } from 'framer-motion'
import { Brain, Code, GraduationCap, Layers } from 'lucide-react'

export default function About() {
  return (
    <div className="min-h-screen bg-slate-50 py-16 px-6">
      <div className="max-w-4xl mx-auto">

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-14"
        >
          <h1 className="text-4xl font-extrabold text-slate-800 mb-4">
            About This System
          </h1>
          <p className="text-slate-500 text-lg max-w-2xl mx-auto">
            A complete rule-based Expert System built from scratch in Python
            with a modern React frontend
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-6">
          {[
            {
              icon : GraduationCap,
              title: "Academic Project",
              color: "text-blue-600 bg-blue-100",
              items: [
                "BS Computer Science — 4th Semester",
                "Course: Artificial Intelligence",
                "Term Project: Expert System",
                "Deadline: May 31, 2026",
              ]
            },
            {
              icon : Brain,
              title: "Expert System",
              color: "text-violet-600 bg-violet-100",
              items: [
                "70+ rules in knowledge base",
                "Forward chaining inference",
                "Certainty factor arithmetic",
                "Conflict resolution strategy",
              ]
            },
            {
              icon : Code,
              title: "Technology Stack",
              color: "text-green-600 bg-green-100",
              items: [
                "Python 3.13.2 — Backend",
                "Flask — REST API",
                "React + Vite — Frontend",
                "Tailwind CSS — Styling",
              ]
            },
            {
              icon : Layers,
              title: "System Components",
              color: "text-orange-600 bg-orange-100",
              items: [
                "Custom rule engine (8 classes)",
                "Input validation module",
                "Output processing module",
                "Explanation module",
              ]
            },
          ].map(({ icon: Icon, title, color, items }, i) => (
            <motion.div
              key={title}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100"
            >
              <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${color}`}>
                <Icon size={22} />
              </div>
              <h3 className="font-bold text-slate-800 mb-3">{title}</h3>
              <ul className="space-y-2">
                {items.map(item => (
                  <li key={item} className="flex items-center gap-2 text-sm text-slate-600">
                    <span className="w-1.5 h-1.5 bg-slate-400 rounded-full flex-shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-8 bg-amber-50 border border-amber-200 rounded-2xl p-6 text-center"
        >
          <p className="text-amber-800 text-sm font-medium">
            ⚠️ Disclaimer: This system is for academic advisory purposes only.
            Always consult a qualified academic advisor for official guidance.
          </p>
        </motion.div>
      </div>
    </div>
  )
}