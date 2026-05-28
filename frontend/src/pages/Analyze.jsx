import { useState }         from 'react'
import { useNavigate }      from 'react-router-dom'
import { motion }           from 'framer-motion'
import { useApp }           from '../context/AppContext'
import { analyzeStudent }   from '../services/api'
import toast                from 'react-hot-toast'
import { Brain, Loader2 }   from 'lucide-react'

// Reusable slider component
function Slider({ label, name, min, max, step, value, onChange, help }) {
  const pct = ((value - min) / (max - min)) * 100
  const color = value < 60 ? '#dc2626' : value < 75 ? '#d97706' : '#059669'

  return (
    <div className="mb-5">
      <div className="flex justify-between items-center mb-1">
        <label className="text-sm font-semibold text-slate-700">{label}</label>
        <span className="text-sm font-bold px-2 py-0.5 rounded-lg text-white"
              style={{ backgroundColor: color }}>
          {value}{name.includes('hour') ? ' hrs' : '%'}
        </span>
      </div>
      <input
        type="range" min={min} max={max} step={step}
        value={value}
        onChange={e => onChange(name, parseFloat(e.target.value))}
        className="w-full h-2 rounded-full appearance-none cursor-pointer"
        style={{ accentColor: color }}
      />
      {help && <p className="text-xs text-slate-400 mt-1">{help}</p>}
    </div>
  )
}

// Section card wrapper
function Section({ title, emoji, children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 mb-6"
    >
      <h3 className="text-base font-bold text-slate-800 mb-5 pb-3 border-b border-slate-100">
        {emoji} {title}
      </h3>
      {children}
    </motion.div>
  )
}

export default function Analyze() {
  const navigate = useNavigate()
  const { setResults, setStudentData, setLoading, loading } = useApp()

  const [form, setForm] = useState({
    name                      : '',
    student_id                : '',
    semester                  : 4,
    midterm_score             : 65,
    assignment_completion_rate: 75,
    quiz_average              : 60,
    lab_completion_rate       : 70,
    prev_semester_avg         : 65,
    failed_subjects_count     : 0,
    academic_trend            : 'stable',
    attendance                : 80,
    days_absent_consecutively : 0,
    attendance_trend          : 'stable',
    study_hours_per_day       : 2,
    participation_level       : 50,
    has_part_time_job         : false,
    financial_stress_level    : 2,
    health_issues             : false,
    family_responsibilities   : 1,
  })

  const update = (key, val) => setForm(prev => ({ ...prev, [key]: val }))

  const handleSubmit = async (e) => {
  e.preventDefault()

  if (!form.name.trim()) {
    toast.error('Please enter student name')
    return
  }
  if (!form.student_id.trim()) {
    toast.error('Please enter student ID')
    return
  }

  console.log('=== SENDING DATA TO API ===')
  console.log('Form data:', form)

  setLoading(true)
  try {
    const res = await analyzeStudent(form)
    
    console.log('=== API RESPONSE ===')
    console.log('Full response:', res)
    console.log('Success?', res.success)
    console.log('Risk Score:', res.risk_score)
    console.log('Performance Level:', res.performance_level)
    
    if (res.success) {
      setResults(res)
      setStudentData(form)
      toast.success('Analysis complete!')
      navigate('/results')
    } else {
      console.error('API returned errors:', res.errors)
      toast.error(res.errors?.[0] || 'Analysis failed')
    }
  } catch (err) {
    console.error('=== CONNECTION ERROR ===')
    console.error('Error details:', err)
    toast.error('Cannot connect to server. Is Flask running?')
  } finally {
    setLoading(false)
  }
}

  return (
    <div className="min-h-screen bg-slate-50 py-10 px-6">
      <div className="max-w-4xl mx-auto">

        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-3xl font-extrabold text-slate-800 mb-2">
            Student Performance Analysis
          </h1>
          <p className="text-slate-500">
            Fill in the student details below to get an AI-powered prediction
          </p>
        </div>

        <form onSubmit={handleSubmit}>

          {/* Personal Info */}
          <Section title="Personal Information" emoji="👤">
            <div className="grid md:grid-cols-3 gap-4">
              <div>
                <label className="text-sm font-semibold text-slate-700 block mb-1">
                  Student Name *
                </label>
                <input
                  type="text"
                  value={form.name}
                  onChange={e => update('name', e.target.value)}
                  placeholder="e.g. Ali Hassan"
                  className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="text-sm font-semibold text-slate-700 block mb-1">
                  Student ID *
                </label>
                <input
                  type="text"
                  value={form.student_id}
                  onChange={e => update('student_id', e.target.value)}
                  placeholder="e.g. F21-001"
                  className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="text-sm font-semibold text-slate-700 block mb-1">
                  Semester
                </label>
                <select
                  value={form.semester}
                  onChange={e => update('semester', parseInt(e.target.value))}
                  className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {[1,2,3,4,5,6,7,8].map(s => (
                    <option key={s} value={s}>Semester {s}</option>
                  ))}
                </select>
              </div>
            </div>
          </Section>

          {/* Academic Performance */}
          <Section title="Academic Performance" emoji="📚">
            <div className="grid md:grid-cols-2 gap-x-8">
              <Slider label="Midterm Exam Score (%)"        name="midterm_score"              min={0} max={100} step={1} value={form.midterm_score}              onChange={update} help="Score obtained in midterm exam" />
              <Slider label="Assignment Completion (%)"     name="assignment_completion_rate"  min={0} max={100} step={1} value={form.assignment_completion_rate}  onChange={update} help="Percentage of assignments submitted" />
              <Slider label="Quiz Average (%)"              name="quiz_average"               min={0} max={100} step={1} value={form.quiz_average}               onChange={update} help="Average score across all quizzes" />
              <Slider label="Lab Work Completion (%)"       name="lab_completion_rate"         min={0} max={100} step={1} value={form.lab_completion_rate}         onChange={update} help="Lab work completion rate" />
              <Slider label="Previous Semester Average (%)" name="prev_semester_avg"           min={0} max={100} step={1} value={form.prev_semester_avg}           onChange={update} help="Last semester average score" />
              <div>
                <label className="text-sm font-semibold text-slate-700 block mb-1">Failed Subjects (History)</label>
                <input
                  type="number" min={0} max={10}
                  value={form.failed_subjects_count}
                  onChange={e => update('failed_subjects_count', parseInt(e.target.value))}
                  className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
            <div className="mt-2">
              <label className="text-sm font-semibold text-slate-700 block mb-1">Academic Trend</label>
              <div className="flex gap-3">
                {['improving','stable','declining'].map(t => (
                  <button type="button" key={t}
                    onClick={() => update('academic_trend', t)}
                    className={`flex-1 py-2 rounded-xl text-sm font-semibold capitalize transition-all
                      ${form.academic_trend === t
                        ? 'bg-blue-600 text-white shadow-md'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}
                  >
                    {t === 'improving' ? '📈' : t === 'stable' ? '➡️' : '📉'} {t}
                  </button>
                ))}
              </div>
            </div>
          </Section>

          {/* Attendance */}
          <Section title="Attendance" emoji="📅">
            <div className="grid md:grid-cols-2 gap-x-8">
              <Slider label="Attendance (%)" name="attendance" min={0} max={100} step={1} value={form.attendance} onChange={update} help="Overall attendance percentage" />
              <div>
                <label className="text-sm font-semibold text-slate-700 block mb-1">
                  Consecutive Days Absent
                </label>
                <input
                  type="number" min={0} max={30}
                  value={form.days_absent_consecutively}
                  onChange={e => update('days_absent_consecutively', parseInt(e.target.value))}
                  className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
            <div className="mt-2">
              <label className="text-sm font-semibold text-slate-700 block mb-1">Attendance Trend</label>
              <div className="flex gap-3">
                {['improving','stable','declining'].map(t => (
                  <button type="button" key={t}
                    onClick={() => update('attendance_trend', t)}
                    className={`flex-1 py-2 rounded-xl text-sm font-semibold capitalize transition-all
                      ${form.attendance_trend === t
                        ? 'bg-blue-600 text-white shadow-md'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}
                  >
                    {t === 'improving' ? '📈' : t === 'stable' ? '➡️' : '📉'} {t}
                  </button>
                ))}
              </div>
            </div>
          </Section>

          {/* Behavioral */}
          <Section title="Behavioral Factors" emoji="🧍">
            <div className="grid md:grid-cols-2 gap-x-8">
              <Slider label="Study Hours Per Day" name="study_hours_per_day" min={0} max={12} step={0.5} value={form.study_hours_per_day} onChange={update} help="Average daily study hours" />
              <Slider label="Class Participation (%)" name="participation_level" min={0} max={100} step={5} value={form.participation_level} onChange={update} help="How actively student participates" />
            </div>
            <div
              onClick={() => update('has_part_time_job', !form.has_part_time_job)}
              className={`flex items-center justify-between p-4 rounded-xl border-2 cursor-pointer transition-all mt-2
                ${form.has_part_time_job
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-slate-200 bg-white hover:border-slate-300'}`}
            >
              <div>
                <div className="font-semibold text-slate-800 text-sm">Has Part-Time Job</div>
                <div className="text-xs text-slate-500">Student works part-time alongside studies</div>
              </div>
              <div className={`w-12 h-6 rounded-full transition-all ${form.has_part_time_job ? 'bg-blue-500' : 'bg-slate-300'}`}>
                <div className={`w-5 h-5 bg-white rounded-full shadow mt-0.5 transition-all ${form.has_part_time_job ? 'ml-6' : 'ml-0.5'}`} />
              </div>
            </div>
          </Section>

          {/* Personal Factors */}
          <Section title="Personal Factors" emoji="👤">
            <div className="grid md:grid-cols-3 gap-4 mb-4">
              <div>
                <label className="text-sm font-semibold text-slate-700 block mb-2">
                  Financial Stress Level
                </label>
                <div className="flex gap-1">
                  {[1,2,3,4,5].map(n => (
                    <button type="button" key={n}
                      onClick={() => update('financial_stress_level', n)}
                      className={`flex-1 py-2 rounded-lg text-xs font-bold transition-all
                        ${form.financial_stress_level >= n
                          ? 'bg-orange-500 text-white'
                          : 'bg-slate-100 text-slate-400'}`}
                    >
                      {n}
                    </button>
                  ))}
                </div>
                <p className="text-xs text-slate-400 mt-1">1 = Low · 5 = Extreme</p>
              </div>

              <div>
                <label className="text-sm font-semibold text-slate-700 block mb-2">
                  Family Responsibilities
                </label>
                <div className="flex gap-1">
                  {[0,1,2,3,4,5].map(n => (
                    <button type="button" key={n}
                      onClick={() => update('family_responsibilities', n)}
                      className={`flex-1 py-2 rounded-lg text-xs font-bold transition-all
                        ${form.family_responsibilities >= n && n > 0
                          ? 'bg-violet-500 text-white'
                          : n === 0 && form.family_responsibilities === 0
                          ? 'bg-violet-500 text-white'
                          : 'bg-slate-100 text-slate-400'}`}
                    >
                      {n}
                    </button>
                  ))}
                </div>
                <p className="text-xs text-slate-400 mt-1">0 = None · 5 = Very High</p>
              </div>

              <div
                onClick={() => update('health_issues', !form.health_issues)}
                className={`flex items-center justify-between p-4 rounded-xl border-2 cursor-pointer transition-all
                  ${form.health_issues
                    ? 'border-red-400 bg-red-50'
                    : 'border-slate-200 bg-white hover:border-slate-300'}`}
              >
                <div>
                  <div className="font-semibold text-slate-800 text-sm">Health Issues</div>
                  <div className="text-xs text-slate-500">Ongoing health problems</div>
                </div>
                <div className={`w-12 h-6 rounded-full transition-all ${form.health_issues ? 'bg-red-400' : 'bg-slate-300'}`}>
                  <div className={`w-5 h-5 bg-white rounded-full shadow mt-0.5 transition-all ${form.health_issues ? 'ml-6' : 'ml-0.5'}`} />
                </div>
              </div>
            </div>
          </Section>

          {/* Submit */}
          <motion.button
            type="submit"
            disabled={loading}
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            className="w-full bg-gradient-to-r from-blue-600 to-violet-600 text-white font-bold py-5 rounded-2xl text-lg shadow-lg hover:shadow-xl transition-all duration-200 disabled:opacity-60 flex items-center justify-center gap-3"
          >
            {loading ? (
              <>
                <Loader2 size={22} className="animate-spin" />
                Analyzing with AI Expert System...
              </>
            ) : (
              <>
                <Brain size={22} />
                Analyze Performance
              </>
            )}
          </motion.button>
        </form>
      </div>
    </div>
  )
}