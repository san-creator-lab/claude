import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Vacatures from './pages/Vacatures'
import VacatureDetail from './pages/VacatureDetail'
import Contact from './pages/Contact'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/vacatures" element={<Vacatures />} />
        <Route path="/vacatures/:slug" element={<VacatureDetail />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
    </Layout>
  )
}

export default App
