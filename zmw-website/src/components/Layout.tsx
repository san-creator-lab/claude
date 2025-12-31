import { ReactNode } from 'react'
import Navigation from './Navigation'
import Footer from './Footer'
import StickyCTA from './StickyCTA'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen flex flex-col">
      <Navigation />
      <main className="flex-1">
        {children}
      </main>
      <Footer />
      <StickyCTA />
    </div>
  )
}
