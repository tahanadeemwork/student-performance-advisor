import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AppProvider } from './context/AppContext'
import Navbar  from './components/Navbar'
import Footer  from './components/Footer'
import Home    from './pages/Home'
import Analyze from './pages/Analyze'
import Results from './pages/Results'
import About   from './pages/About'

export default function App() {
  return (
    <AppProvider>
      <BrowserRouter>
        <div className="min-h-screen flex flex-col">
          <Navbar />
          <main className="flex-1">
            <Routes>
              <Route path="/"        element={<Home />}    />
              <Route path="/analyze" element={<Analyze />} />
              <Route path="/results" element={<Results />} />
              <Route path="/about"   element={<About />}   />
            </Routes>
          </main>
          <Footer />
        </div>
        <Toaster position="top-right" />
      </BrowserRouter>
    </AppProvider>
  )
}