import { useNavigate }    from 'react-router-dom'
import { motion }         from 'framer-motion'
import { useApp }         from '../context/AppContext'
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis,
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, ReferenceLine
} from 'recharts'
import {
  ArrowLeft, Download, RefreshCw,
  AlertTriangle, CheckCircle, TrendingUp,
  Brain, ChevronDown, ChevronUp
} from 'lucide-react'
import { useState } from 'react'

// Gauge component
function Gauge({ score }) {
  const color = score >= 75 ? '#dc2626' : score >= 50 ? '#ea580c' : score >= 25 ? '#d97706' : '#059669'
  const rotation = (score / 100) * 180 - 90

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-40 h-24 overflow-hidden">
        <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-40 h-40 rounded-full border-8 border-slate-100" />
        <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-40 h-40 rounded-full border-8"
             style={{ borderColor: color, clipPath: 'polygon(0 50%, 100% 50%, 100% 100%, 0 100%)' }} />
        <div className="absolute bottom-0 left-1/2 w-1 h-16 origin-bottom rounded-full"
             style={{ background: color, transform: `translateX(-50%) rotate(${rotation}deg)` }} />
        <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-4 h-4 rounded-full bg-slate-800" />
      </div>
      <div className="text-3xl font-extrabold mt-2" style={{ color }}>
        {score}<span className="text-lg">/100</span>
      </div>
      <div className="text-sm text-slate-500 mt-1">Risk Score</div>
    </div>
  )
}

// Level config
const levelConfig = {
  EXCELLENT : { bg: 'bg-emerald-50', border: 'border-emerald-400', text: 'text-emerald-700', badge: 'bg-emerald-100 text-emerald-700' },
  GOOD      : { bg: 'bg-blue-50',    border: 'border-blue-400',    text: 'text-blue-700',    badge: 'bg-blue-100 text-blue-700'    },
  AVERAGE   : { bg: 'bg-amber-50',   border: 'border-amber-400',   text: 'text-amber-700',   badge: 'bg-amber-100 text-amber-700'  },
  AT_RISK   : { bg: 'bg-orange-50',  border: 'border-orange-400',  text: 'text-orange-700',  badge: 'bg-orange-100 text-orange-700'},
  FAILING   : { bg: 'bg-red-50',     border: 'border-red-400',     text: 'text-red-700',     badge: 'bg-red-100 text-red-700'     },
  Unknown   : { bg: 'bg-slate-50',   border: 'border-slate-300',   text: 'text-slate-700',   badge: 'bg-slate-100 text-slate-700' },
}

export default function Results() {
  const navigate = useNavigate()
  const { results, clearResults } = useApp()
  const [expandedTrace, setExpandedTrace] = useState(null)

  if (!results) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4">
        <p className="text-slate-500 text-lg">No results yet.</p>
        <button
          onClick={() => navigate('/analyze')}
          className="flex items-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-xl font-semibold"
        >
          <ArrowLeft size={18} /> Go to Analyze
        </button>
      </div>
    )
  }

  const cfg = levelConfig[results.performance_level] || levelConfig.Unknown

  // Radar data
  const radarData = [
    { subject: 'Attendance',   value: results.attendance     || 0 },
    { subject: 'Midterm',      value: results.midterm_score  || 0 },
    { subject: 'Assignments',  value: results.assignment_rate|| 0 },
    { subject: 'Quizzes',      value: results.quiz_average   || 0 },
    { subject: 'Study',        value: Math.min((results.study_hours || 0) / 8 * 100, 100) },
    { subject: 'Participate',  value: results.participation  || 0 },
  ]

  // Bar data
  const barData = [
    { name: 'Attendance',  value: results.attendance,      fill: results.attendance   < 60 ? '#dc2626' : results.attendance   < 75 ? '#d97706' : '#059669' },
    { name: 'Midterm',     value: results.midterm_score,   fill: results.midterm_score  < 60 ? '#dc2626' : results.midterm_score  < 75 ? '#d97706' : '#059669' },
    { name: 'Assignments', value: results.assignment_rate, fill: results.assignment_rate < 60 ? '#dc2626' : results.assignment_rate < 75 ? '#d97706' : '#059669' },
    { name: 'Quizzes',    value: results.quiz_average,    fill: results.quiz_average   < 60 ? '#dc2626' : results.quiz_average   < 75 ? '#d97706' : '#059669' },
    { name: 'Prev Avg',   value: results.prev_avg,        fill: results.prev_avg       < 60 ? '#dc2626' : results.prev_avg       < 75 ? '#d97706' : '#059669' },
  ]

  const priorityBadge = {
    URGENT : 'bg-red-100 text-red-700 border border-red-200',
    HIGH   : 'bg-orange-100 text-orange-700 border border-orange-200',
    MEDIUM : 'bg-amber-100 text-amber-700 border border-amber-200',
    LOW    : 'bg-green-100 text-green-700 border border-green-200',
  }

  return (
    <div className="min-h-screen bg-slate-50 py-10 px-6">
      <div className="max-w-6xl mx-auto">

        {/* Back button */}
        <div className="flex items-center gap-3 mb-6">
          <button
            onClick={() => navigate('/analyze')}
            className="flex items-center gap-2 text-slate-500 hover:text-slate-800 transition-colors text-sm font-medium"
          >
            <ArrowLeft size={16} /> Back to Analyze
          </button>
        </div>

        {/* Verdict Banner */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className={`${cfg.bg} border-2 ${cfg.border} rounded-2xl p-6 mb-8`}
        >
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <span className="text-4xl">{results.performance_emoji}</span>
                <div>
                  <h1 className={`text-2xl font-extrabold ${cfg.text}`}>
                    {results.performance_label}
                  </h1>
                  <p className="text-slate-600 text-sm">{results.performance_desc}</p>
                </div>
              </div>
              <p className="text-slate-500 text-sm">
                {results.student_name} · ID: {results.student_id} ·
                Semester {results.semester} · {results.generated_at}
              </p>
            </div>
            <div className="flex items-center gap-3">
              <span className={`px-4 py-2 rounded-full text-sm font-bold ${priorityBadge[results.intervention_priority]}`}>
                {results.intervention_priority} PRIORITY
              </span>
              <span className={`px-4 py-2 rounded-full text-sm font-bold ${cfg.badge}`}>
                Risk: {results.risk_score}/100
              </span>
            </div>
          </div>
        </motion.div>

        {/* Top Row — Gauge + Metrics */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">

          {/* Gauge */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex items-center justify-center"
          >
            <Gauge score={results.risk_score} />
          </motion.div>

          {/* Metrics */}
          {[
            { label: 'Attendance',   value: results.attendance,      suffix: '%' },
            { label: 'Midterm Score', value: results.midterm_score,   suffix: '%' },
            { label: 'Assignments',  value: results.assignment_rate,  suffix: '%' },
          ].map(({ label, value, suffix }, i) => (
            <motion.div
              key={label}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 text-center"
            >
              <div className={`text-3xl font-extrabold mb-1 ${
                value < 60 ? 'text-red-600' : value < 75 ? 'text-amber-600' : 'text-green-600'
              }`}>
                {value}{suffix}
              </div>
              <div className="text-slate-500 text-sm font-medium">{label}</div>
              <div className={`mt-2 text-xs font-semibold px-2 py-0.5 rounded-full inline-block ${
                value < 60 ? 'bg-red-100 text-red-600' :
                value < 75 ? 'bg-amber-100 text-amber-600' : 'bg-green-100 text-green-600'
              }`}>
                {value < 60 ? '⚠️ Low' : value < 75 ? '📊 Average' : '✅ Good'}
              </div>
            </motion.div>
          ))}
        </div>

        {/* Charts Row */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">

          {/* Radar Chart */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100"
          >
            <h3 className="font-bold text-slate-800 mb-4">📡 Student Profile Radar</h3>
            <ResponsiveContainer width="100%" height={280}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="#e2e8f0" />
                <PolarAngleAxis dataKey="subject" tick={{ fontSize: 12, fill: '#64748b' }} />
                <Radar
                  dataKey="value"
                  stroke="#2563eb"
                  fill="#2563eb"
                  fillOpacity={0.15}
                  strokeWidth={2}
                />
              </RadarChart>
            </ResponsiveContainer>
          </motion.div>

          {/* Bar Chart */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100"
          >
            <h3 className="font-bold text-slate-800 mb-4">📊 Performance by Metric</h3>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={barData} margin={{ top: 10, right: 10, bottom: 0, left: -10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#64748b' }} />
                <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: '#64748b' }} />
                <Tooltip formatter={(v) => [`${v}%`]} />
                <ReferenceLine y={60} stroke="#ef4444" strokeDasharray="4 4" label={{ value: "Min 60%", fontSize: 10, fill: '#ef4444' }} />
                <ReferenceLine y={75} stroke="#f59e0b" strokeDasharray="4 4" label={{ value: "Target 75%", fontSize: 10, fill: '#f59e0b' }} />
                <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                  {barData.map((entry, i) => (
                    <rect key={i} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </motion.div>
        </div>

        {/* Risk Factors + Strengths */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">

          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100"
          >
            <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
              <AlertTriangle size={18} className="text-orange-500" />
              Primary Risk Factors
            </h3>
            {results.risk_factors?.length > 0 ? (
              <div className="space-y-2">
                {results.risk_factors.map((f, i) => (
                  <div key={i} className="bg-orange-50 border border-orange-100 rounded-xl px-4 py-3 text-sm text-slate-700">
                    {f}
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-green-600 text-sm font-medium">
                ✅ No significant risk factors identified
              </div>
            )}
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100"
          >
            <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
              <CheckCircle size={18} className="text-green-500" />
              Identified Strengths
            </h3>
            {results.strengths?.length > 0 ? (
              <div className="space-y-2">
                {results.strengths.map((s, i) => (
                  <div key={i} className="bg-green-50 border border-green-100 rounded-xl px-4 py-3 text-sm text-slate-700">
                    {s}
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-slate-500 text-sm">
                Keep working — strengths will develop
              </div>
            )}
          </motion.div>
        </div>

        {/* Recommendations */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 mb-8"
        >
          <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
            <TrendingUp size={18} className="text-blue-500" />
            Personalized Recommendations
          </h3>
          {results.recommendations?.length > 0 ? (
            <div className="space-y-3">
              {results.recommendations.map((rec, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.07 }}
                  className="flex items-start gap-3 bg-blue-50 border border-blue-100 rounded-xl px-4 py-3"
                >
                  <span className="text-blue-500 mt-0.5 flex-shrink-0">💡</span>
                  <span className="text-sm text-slate-700">{rec}</span>
                </motion.div>
              ))}
            </div>
          ) : (
            <div className="text-green-600 font-medium text-sm">
              ✅ Continue current performance — you are doing great!
            </div>
          )}
        </motion.div>

        {/* Reasoning Chain */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 mb-8"
        >
          <h3 className="font-bold text-slate-800 mb-2 flex items-center gap-2">
            <Brain size={18} className="text-violet-500" />
            AI Reasoning Chain
            <span className="text-xs font-normal text-slate-400 ml-auto">
              {results.rules_fired} of {results.total_rules} rules fired
            </span>
          </h3>
          <p className="text-slate-500 text-xs mb-4">
            Every step the expert system took to reach its conclusion
          </p>

          {results.reasoning_trace?.length > 0 ? (
            <div className="space-y-2">
              {results.reasoning_trace.map((entry, i) => (
                <div key={i} className="border border-slate-100 rounded-xl overflow-hidden">
                  <button
                    onClick={() => setExpandedTrace(expandedTrace === i ? null : i)}
                    className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-slate-50 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <span className="w-7 h-7 bg-violet-100 text-violet-600 rounded-lg flex items-center justify-center text-xs font-bold flex-shrink-0">
                        {entry.step}
                      </span>
                      <span className="text-sm font-medium text-slate-700">
                        {entry.rule}
                      </span>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-xs font-bold text-violet-600 bg-violet-50 px-2 py-1 rounded-lg">
                        {entry.cf_percent}
                      </span>
                      {expandedTrace === i
                        ? <ChevronUp size={16} className="text-slate-400" />
                        : <ChevronDown size={16} className="text-slate-400" />
                      }
                    </div>
                  </button>

                  {expandedTrace === i && (
                    <div className="px-4 pb-4 bg-slate-50 border-t border-slate-100">
                      <div className="mt-3 space-y-2">
                        <div>
                          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Condition</span>
                          <p className="text-sm text-slate-700 mt-1 bg-white border border-slate-100 rounded-lg px-3 py-2">
                            {entry.description}
                          </p>
                        </div>
                        <div>
                          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Conclusion</span>
                          <p className="text-sm text-green-700 mt-1 bg-green-50 border border-green-100 rounded-lg px-3 py-2">
                            {entry.conclusion}
                          </p>
                        </div>
                        <div>
                          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wide">
                            Confidence: {entry.cf_percent}
                          </span>
                          <div className="w-full bg-slate-200 rounded-full h-2 mt-1">
                            <div
                              className="bg-violet-500 h-2 rounded-full transition-all"
                              style={{ width: entry.cf_percent }}
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="text-slate-400 text-sm">No reasoning trace available</div>
          )}
        </motion.div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4">
          <button
            onClick={() => {
              const blob = new Blob([results.console_report || ''], { type: 'text/plain' })
              const url  = URL.createObjectURL(blob)
              const a    = document.createElement('a')
              a.href     = url
              a.download = `report_${results.student_id}.txt`
              a.click()
            }}
            className="flex-1 flex items-center justify-center gap-2 bg-slate-800 text-white font-semibold py-4 rounded-2xl hover:bg-slate-700 transition-colors"
          >
            <Download size={18} />
            Download Report
          </button>

          <button
            onClick={() => { clearResults(); navigate('/analyze') }}
            className="flex-1 flex items-center justify-center gap-2 bg-blue-600 text-white font-semibold py-4 rounded-2xl hover:bg-blue-700 transition-colors"
          >
            <RefreshCw size={18} />
            Analyze Another Student
          </button>
        </div>
      </div>
    </div>
  )
}