import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Brain, ChartBar, FileText,
  ArrowRight, CheckCircle, Zap,
  Shield, Users, TrendingUp
} from 'lucide-react'

const features = [
  {
    icon  : Brain,
    title : "70+ Expert Rules",
    desc  : "Knowledge base with rules covering academic, behavioral, and personal factors",
    color : "bg-blue-100 text-blue-600"
  },
  {
    icon  : Zap,
    title : "Forward Chaining",
    desc  : "Real inference engine that reasons step by step just like a human expert",
    color : "bg-violet-100 text-violet-600"
  },
  {
    icon  : Shield,
    title : "Certainty Factors",
    desc  : "Every conclusion comes with a confidence score from 0 to 100 percent",
    color : "bg-green-100 text-green-600"
  },
  {
    icon  : ChartBar,
    title : "Visual Analytics",
    desc  : "Radar charts, bar charts, and gauge charts for clear data visualization",
    color : "bg-orange-100 text-orange-600"
  },
  {
    icon  : FileText,
    title : "Explainable AI",
    desc  : "Full reasoning chain showing exactly why every conclusion was reached",
    color : "bg-pink-100 text-pink-600"
  },
  {
    icon  : TrendingUp,
    title : "Personalized Plans",
    desc  : "Specific, actionable recommendations tailored to each student",
    color : "bg-cyan-100 text-cyan-600"
  },
]

const steps = [
  { num: "01", title: "Enter Student Data",   desc: "Fill in academic, attendance, and personal information" },
  { num: "02", title: "AI Analysis",          desc: "Expert system runs 70+ rules using forward chaining" },
  { num: "03", title: "Get Results",          desc: "Receive prediction, risk factors, and recommendations" },
]

export default function Home() {
  return (
    <div className="min-h-screen">

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-900 via-blue-700 to-violet-700 text-white py-24 px-6">
        <div className="max-w-5xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-block bg-white/15 border border-white/25 px-5 py-2 rounded-full text-sm font-medium mb-6">
              🎓 AI-Powered Academic Advisory System
            </div>

            <h1 className="text-5xl md:text-6xl font-extrabold mb-6 leading-tight">
              Student Performance
              <span className="block text-blue-200">
                Prediction Advisor
              </span>
            </h1>

            <p className="text-xl text-blue-100 max-w-2xl mx-auto mb-10">
              An intelligent rule-based expert system that predicts academic
              performance, identifies risk factors, and provides personalized
              recommendations with explainable AI reasoning.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/analyze"
                className="flex items-center justify-center gap-2 bg-white text-blue-700 font-bold px-8 py-4 rounded-xl hover:bg-blue-50 transition-all duration-200 shadow-lg hover:shadow-xl hover:-translate-y-0.5"
              >
                Start Analysis
                <ArrowRight size={18} />
              </Link>
              <Link
                to="/about"
                className="flex items-center justify-center gap-2 bg-white/15 border border-white/30 text-white font-semibold px-8 py-4 rounded-xl hover:bg-white/25 transition-all duration-200"
              >
                Learn More
              </Link>
            </div>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.5 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-16"
          >
            {[
              { num: "70+",  label: "Expert Rules" },
              { num: "5",    label: "Rule Categories" },
              { num: "10+",  label: "Test Scenarios" },
              { num: "100%", label: "Explainable" },
            ].map(({ num, label }) => (
              <div key={label} className="bg-white/10 backdrop-blur rounded-2xl p-5 border border-white/20">
                <div className="text-3xl font-extrabold">{num}</div>
                <div className="text-blue-200 text-sm mt-1">{label}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-6 bg-white">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl font-extrabold text-slate-800 mb-3">
              How It Works
            </h2>
            <p className="text-slate-500 text-lg">
              Three simple steps to get your complete academic analysis
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {steps.map(({ num, title, desc }, i) => (
              <motion.div
                key={num}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.15 }}
                viewport={{ once: true }}
                className="text-center"
              >
                <div className="w-16 h-16 bg-gradient-to-br from-blue-600 to-violet-600 text-white rounded-2xl flex items-center justify-center text-xl font-extrabold mx-auto mb-5 shadow-lg">
                  {num}
                </div>
                <h3 className="text-lg font-bold text-slate-800 mb-2">{title}</h3>
                <p className="text-slate-500 text-sm leading-relaxed">{desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 px-6 bg-slate-50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl font-extrabold text-slate-800 mb-3">
              System Features
            </h2>
            <p className="text-slate-500 text-lg">
              A complete expert system built from scratch
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map(({ icon: Icon, title, desc, color }, i) => (
              <motion.div
                key={title}
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ y: -4 }}
                className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition-all duration-200"
              >
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${color}`}>
                  <Icon size={22} />
                </div>
                <h3 className="font-bold text-slate-800 mb-2">{title}</h3>
                <p className="text-slate-500 text-sm leading-relaxed">{desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6 bg-gradient-to-r from-blue-600 to-violet-600 text-white text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl font-extrabold mb-4">
            Ready to Analyze Performance?
          </h2>
          <p className="text-blue-100 mb-8 text-lg">
            Get instant AI-powered insights for any student
          </p>
          <Link
            to="/analyze"
            className="inline-flex items-center gap-2 bg-white text-blue-700 font-bold px-10 py-4 rounded-xl hover:bg-blue-50 transition-all duration-200 shadow-lg"
          >
            Start Now
            <ArrowRight size={18} />
          </Link>
        </motion.div>
      </section>
    </div>
  )
}