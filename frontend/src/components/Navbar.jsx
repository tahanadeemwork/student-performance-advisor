import { Link, useLocation } from 'react-router-dom'
import { GraduationCap, Brain, Home, Info } from 'lucide-react'

export default function Navbar() {
  const location = useLocation()

  const links = [
    { to: '/',        label: 'Home',    icon: Home },
    { to: '/analyze', label: 'Analyze', icon: Brain },
    { to: '/about',   label: 'About',   icon: Info },
  ]

  return (
    <nav className="bg-gradient-to-r from-blue-900 via-blue-700 to-violet-700 shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

        {/* Logo */}
        <Link to="/" className="flex items-center gap-3 text-white">
          <div className="bg-white/20 p-2 rounded-xl">
            <GraduationCap size={24} />
          </div>
          <div>
            <div className="font-bold text-lg leading-tight">
              Student Advisor
            </div>
            <div className="text-blue-200 text-xs">
              AI Expert System
            </div>
          </div>
        </Link>

        {/* Links */}
        <div className="flex items-center gap-2">
          {links.map(({ to, label, icon: Icon }) => (
            <Link
              key={to}
              to={to}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200
                ${location.pathname === to
                  ? 'bg-white text-blue-700 shadow-md'
                  : 'text-white/80 hover:bg-white/15 hover:text-white'
                }`}
            >
              <Icon size={16} />
              {label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  )
}