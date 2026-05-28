// ============================================
// App Context — Global State Management
// ============================================

import { createContext, useContext, useState } from 'react'

const AppContext = createContext()

export function AppProvider({ children }) {
  const [results,     setResults]     = useState(null)
  const [studentData, setStudentData] = useState(null)
  const [loading,     setLoading]     = useState(false)
  const [error,       setError]       = useState(null)

  const clearResults = () => {
    setResults(null)
    setStudentData(null)
    setError(null)
  }

  return (
    <AppContext.Provider value={{
      results,     setResults,
      studentData, setStudentData,
      loading,     setLoading,
      error,       setError,
      clearResults
    }}>
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => useContext(AppContext)