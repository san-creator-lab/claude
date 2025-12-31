import { useEffect, useRef, useState } from 'react'
import { cn } from '@/lib/utils'
import AnimatedSection from '../AnimatedSection'

const metrics = [
  {
    id: 'year',
    value: 1960,
    label: 'Opgericht',
    format: 'year',
    description: 'Familiebedrijf met jarenlange expertise',
  },
  {
    id: 'machines',
    value: 35,
    suffix: '+',
    label: 'CNC-machines',
    format: 'number',
    description: 'Draai- en freesmachines',
  },
  {
    id: 'facility',
    value: 2679,
    label: 'm² faciliteit',
    format: 'number',
    description: 'Moderne productiefaciliteit',
  },
  {
    id: 'experience',
    value: 60,
    suffix: '+',
    label: 'Jaar ervaring',
    format: 'number',
    description: 'In CNC verspaning',
  },
]

export default function Metrics() {
  return (
    <section className="section-padding bg-graphite-950 relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 precision-grid opacity-20" />
        <div className="absolute bottom-0 left-0 w-full h-1/2 bg-gradient-to-t from-graphite-900/50 to-transparent" />
      </div>

      <div className="container-industrial relative">
        {/* Section Header */}
        <AnimatedSection className="text-center max-w-3xl mx-auto mb-16 md:mb-20">
          <div className="flex items-center justify-center gap-4 mb-6">
            <div className="w-12 h-px bg-accent-500" />
            <span className="text-accent-400 font-mono text-mono uppercase tracking-widest">
              In cijfers
            </span>
            <div className="w-12 h-px bg-accent-500" />
          </div>
          <h2 className="font-heading font-bold text-cream-50 text-heading-xl md:text-display mb-6">
            Bewezen expertise
          </h2>
          <p className="text-cream-300 text-body-lg">
            Meer dan 60 jaar vakmanschap. Een echt familiebedrijf waar klanten dit voelen
            vanaf het eerste contact en gedurende de gehele samenwerking.
          </p>
        </AnimatedSection>

        {/* Metrics Grid - Spec Sheet Style */}
        <div className="max-w-5xl mx-auto">
          <div className="border border-graphite-700 bg-graphite-900/30 backdrop-blur-sm">
            {/* Header row */}
            <div className="grid grid-cols-4 border-b border-graphite-700 bg-graphite-800/30">
              <div className="p-4 text-center border-r border-graphite-700 last:border-r-0">
                <span className="font-mono text-accent-400 text-caption uppercase tracking-wider">
                  Oprichting
                </span>
              </div>
              <div className="p-4 text-center border-r border-graphite-700 last:border-r-0">
                <span className="font-mono text-accent-400 text-caption uppercase tracking-wider">
                  Machines
                </span>
              </div>
              <div className="p-4 text-center border-r border-graphite-700 last:border-r-0">
                <span className="font-mono text-accent-400 text-caption uppercase tracking-wider">
                  Oppervlakte
                </span>
              </div>
              <div className="p-4 text-center">
                <span className="font-mono text-accent-400 text-caption uppercase tracking-wider">
                  Ervaring
                </span>
              </div>
            </div>

            {/* Values row */}
            <div className="grid grid-cols-4">
              {metrics.map((metric, index) => (
                <MetricValue
                  key={metric.id}
                  metric={metric}
                  isLast={index === metrics.length - 1}
                />
              ))}
            </div>

            {/* Descriptions row */}
            <div className="grid grid-cols-4 border-t border-graphite-700 bg-graphite-800/20">
              {metrics.map((metric, index) => (
                <div
                  key={`desc-${metric.id}`}
                  className={cn(
                    'p-4 text-center',
                    index < metrics.length - 1 && 'border-r border-graphite-700'
                  )}
                >
                  <span className="text-cream-400 text-body-sm">
                    {metric.description}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Mobile: Stacked cards */}
        <div className="md:hidden mt-8 space-y-4">
          {metrics.map((metric, index) => (
            <AnimatedSection key={metric.id} delay={index * 100}>
              <div className="border border-graphite-700 bg-graphite-900/30 p-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-mono text-accent-400 text-caption uppercase tracking-wider">
                    {metric.label}
                  </span>
                </div>
                <div className="flex items-baseline gap-1">
                  <span className="font-mono font-bold text-cream-50 text-3xl">
                    {metric.value.toLocaleString('nl-NL')}
                  </span>
                  {metric.suffix && (
                    <span className="font-mono text-accent-400 text-xl">
                      {metric.suffix}
                    </span>
                  )}
                </div>
                <p className="text-cream-400 text-body-sm mt-2">
                  {metric.description}
                </p>
              </div>
            </AnimatedSection>
          ))}
        </div>
      </div>
    </section>
  )
}

interface MetricValueProps {
  metric: typeof metrics[0]
  isLast: boolean
}

function MetricValue({ metric, isLast }: MetricValueProps) {
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
  }, [hasAnimated])

  const animateCount = () => {
    const duration = 2000
    const steps = 60
    const increment = metric.value / steps
    let current = 0
    const stepDuration = duration / steps

    const timer = setInterval(() => {
      current += increment
      if (current >= metric.value) {
        setCount(metric.value)
        clearInterval(timer)
      } else {
        setCount(Math.floor(current))
      }
    }, stepDuration)
  }

  return (
    <div
      ref={ref}
      className={cn(
        'hidden md:flex flex-col items-center justify-center p-8 lg:p-12',
        !isLast && 'border-r border-graphite-700'
      )}
    >
      <div className="flex items-baseline gap-1">
        <span className="font-mono font-bold text-cream-50 text-4xl lg:text-5xl tabular-nums">
          {count.toLocaleString('nl-NL')}
        </span>
        {metric.suffix && (
          <span className="font-mono font-bold text-accent-400 text-2xl lg:text-3xl">
            {metric.suffix}
          </span>
        )}
      </div>
      <span className="text-cream-300 text-body-sm mt-2">
        {metric.label}
      </span>
    </div>
  )
}
