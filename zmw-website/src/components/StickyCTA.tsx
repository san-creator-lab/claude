import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { ChevronRight, X } from 'lucide-react'
import { cn } from '@/lib/utils'

export default function StickyCTA() {
  const [isVisible, setIsVisible] = useState(false)
  const [isDismissed, setIsDismissed] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      const scrollY = window.scrollY
      const threshold = window.innerHeight * 0.5
      setIsVisible(scrollY > threshold)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  if (isDismissed) return null

  return (
    <>
      {/* Desktop: Sticky side button */}
      <div
        className={cn(
          'fixed right-0 top-1/2 -translate-y-1/2 z-40 hidden md:block',
          'transition-all duration-500',
          isVisible
            ? 'translate-x-0 opacity-100'
            : 'translate-x-full opacity-0'
        )}
      >
        <Link
          to="/contact"
          className="group flex items-center bg-accent-500 hover:bg-accent-400 text-graphite-950 font-semibold transition-all duration-300"
        >
          <span className="px-4 py-4 writing-mode-vertical rotate-180 text-body-sm uppercase tracking-widest"
            style={{ writingMode: 'vertical-rl' }}
          >
            Offerte aanvragen
          </span>
          <span className="bg-accent-600 p-4 transition-colors group-hover:bg-accent-500">
            <ChevronRight className="w-5 h-5 -rotate-90" />
          </span>
        </Link>
      </div>

      {/* Mobile: Bottom CTA bar */}
      <div
        className={cn(
          'fixed bottom-0 left-0 right-0 z-40 md:hidden',
          'transition-all duration-500',
          isVisible
            ? 'translate-y-0 opacity-100'
            : 'translate-y-full opacity-0'
        )}
      >
        <div className="bg-graphite-950/95 backdrop-blur-md border-t border-graphite-800/50 p-4">
          <div className="flex items-center gap-3">
            <Link
              to="/contact"
              className="btn-primary flex-1 justify-center py-3"
            >
              <span>Offerte aanvragen</span>
              <ChevronRight className="w-5 h-5 ml-1" />
            </Link>
            <button
              onClick={() => setIsDismissed(true)}
              className="p-3 text-cream-400 hover:text-cream-100 transition-colors"
              aria-label="Sluiten"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </>
  )
}
