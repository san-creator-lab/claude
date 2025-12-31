import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { ChevronRight, ChevronDown } from 'lucide-react'
import { cn } from '@/lib/utils'

export default function Hero() {
  const [isLoaded, setIsLoaded] = useState(false)
  const heroRef = useRef<HTMLElement>(null)

  useEffect(() => {
    setIsLoaded(true)
  }, [])

  const scrollToContent = () => {
    window.scrollTo({
      top: window.innerHeight,
      behavior: 'smooth'
    })
  }

  return (
    <section
      ref={heroRef}
      className="relative min-h-screen flex items-center justify-center overflow-hidden"
    >
      {/* Background with gradient overlay */}
      <div className="absolute inset-0">
        {/* Industrial gradient background */}
        <div className="absolute inset-0 bg-gradient-to-br from-graphite-950 via-graphite-900 to-graphite-950" />

        {/* Precision grid pattern */}
        <div className="absolute inset-0 precision-grid opacity-30" />

        {/* Radial gradient for depth */}
        <div className="absolute inset-0 bg-gradient-radial from-accent-500/5 via-transparent to-transparent" />

        {/* Top gradient fade */}
        <div className="absolute top-0 left-0 right-0 h-40 bg-gradient-to-b from-graphite-950 to-transparent" />

        {/* Bottom gradient fade */}
        <div className="absolute bottom-0 left-0 right-0 h-40 bg-gradient-to-t from-graphite-950 to-transparent" />
      </div>

      {/* Animated accent lines */}
      <div className="absolute inset-0 overflow-hidden">
        <div
          className={cn(
            'absolute top-1/4 left-0 w-1/3 h-px bg-gradient-to-r from-transparent via-accent-500/50 to-transparent',
            'transition-all duration-1000 delay-500',
            isLoaded ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-full'
          )}
        />
        <div
          className={cn(
            'absolute top-3/4 right-0 w-1/4 h-px bg-gradient-to-l from-transparent via-accent-500/50 to-transparent',
            'transition-all duration-1000 delay-700',
            isLoaded ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-full'
          )}
        />
      </div>

      {/* Content */}
      <div className="relative container-industrial py-32 md:py-40">
        <div className="max-w-5xl">
          {/* Eyebrow */}
          <div
            className={cn(
              'flex items-center gap-4 mb-8 transition-all duration-700',
              isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
            )}
          >
            <div className="w-12 h-px bg-accent-500" />
            <span className="text-accent-400 font-mono text-mono uppercase tracking-widest">
              Sinds 1960
            </span>
          </div>

          {/* Main Headline */}
          <h1
            className={cn(
              'font-heading font-bold text-cream-50 mb-6',
              'text-4xl sm:text-5xl md:text-6xl lg:text-display-lg xl:text-display-xl',
              'transition-all duration-700 delay-100',
              isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'
            )}
          >
            Sterk in{' '}
            <span className="text-gradient-accent">CNC draaien</span>
            {' '}&{' '}
            <span className="text-gradient-accent">frezen</span>
          </h1>

          {/* Subheadline */}
          <p
            className={cn(
              'text-cream-300 text-lg md:text-xl lg:text-2xl max-w-2xl mb-10',
              'transition-all duration-700 delay-200',
              isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'
            )}
          >
            Van prototype en enkelstuks tot seriematig in oplages van 250 tot 100.000+.
            Alle gangbare staalsoorten, RVS, messing, aluminium en kunststof.
          </p>

          {/* CTA Buttons */}
          <div
            className={cn(
              'flex flex-col sm:flex-row gap-4',
              'transition-all duration-700 delay-300',
              isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'
            )}
          >
            <Link to="/contact" className="btn-primary group">
              <span>Offerte aanvragen</span>
              <ChevronRight className="w-5 h-5 ml-2 transition-transform group-hover:translate-x-1" />
            </Link>
            <button onClick={scrollToContent} className="btn-secondary group">
              <span>Zo werken we</span>
              <ChevronDown className="w-5 h-5 ml-2 transition-transform group-hover:translate-y-1" />
            </button>
          </div>
        </div>

        {/* Trust Strip */}
        <div
          className={cn(
            'mt-20 md:mt-28 pt-10 border-t border-graphite-700/50',
            'transition-all duration-700 delay-500',
            isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'
          )}
        >
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-12">
            <TrustMetric value={1960} label="Opgericht" prefix="Sinds" />
            <TrustMetric value={35} label="CNC-machines" suffix="+" />
            <TrustMetric value={2679} label="m² productiefaciliteit" />
            <TrustMetric value={60} label="jaar ervaring" suffix="+" />
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <button
        onClick={scrollToContent}
        className={cn(
          'absolute bottom-8 left-1/2 -translate-x-1/2',
          'flex flex-col items-center gap-2 text-cream-400 hover:text-accent-400 transition-colors',
          'transition-all duration-700 delay-700',
          isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
        )}
        aria-label="Scroll naar beneden"
      >
        <span className="text-caption uppercase tracking-widest">Ontdek meer</span>
        <ChevronDown className="w-5 h-5 animate-bounce" />
      </button>
    </section>
  )
}

interface TrustMetricProps {
  value: number
  label: string
  prefix?: string
  suffix?: string
}

function TrustMetric({ value, label, prefix, suffix }: TrustMetricProps) {
  const [count, setCount] = useState(0)
  const [hasAnimated, setHasAnimated] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !hasAnimated) {
          setHasAnimated(true)
          animateCount()
        }
      },
      { threshold: 0.5 }
    )

    if (ref.current) {
      observer.observe(ref.current)
    }

    return () => observer.disconnect()
  }, [hasAnimated, value])

  const animateCount = () => {
    const duration = 2000
    const steps = 60
    const increment = value / steps
    let current = 0
    const stepDuration = duration / steps

    const timer = setInterval(() => {
      current += increment
      if (current >= value) {
        setCount(value)
        clearInterval(timer)
      } else {
        setCount(Math.floor(current))
      }
    }, stepDuration)
  }

  return (
    <div ref={ref} className="text-center md:text-left">
      <div className="flex items-baseline justify-center md:justify-start gap-1">
        {prefix && (
          <span className="text-cream-400 font-mono text-mono">{prefix}</span>
        )}
        <span className="text-cream-50 font-heading font-bold text-3xl md:text-4xl lg:text-heading-xl tabular-nums">
          {count.toLocaleString('nl-NL')}
        </span>
        {suffix && (
          <span className="text-accent-400 font-heading font-bold text-2xl">{suffix}</span>
        )}
      </div>
      <span className="text-cream-400 text-body-sm">{label}</span>
    </div>
  )
}
