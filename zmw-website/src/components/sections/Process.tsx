import { FileText, ThumbsUp, Settings, PackageCheck } from 'lucide-react'
import { cn } from '@/lib/utils'
import AnimatedSection from '../AnimatedSection'

const steps = [
  {
    number: '01',
    icon: FileText,
    title: 'Tekening & Offerte',
    description: 'U stuurt uw tekening of specificaties. Wij maken een scherpe offerte op basis van uw wensen.',
  },
  {
    number: '02',
    icon: ThumbsUp,
    title: 'Opdracht & Planning',
    description: 'Bij akkoord plannen we uw opdracht in. Duidelijke afspraken over levertijd en specificaties.',
  },
  {
    number: '03',
    icon: Settings,
    title: 'Productie & Kwaliteit',
    description: 'Productie op ons moderne CNC machinepark. Kwaliteitscontrole bij elke stap in het proces.',
  },
  {
    number: '04',
    icon: PackageCheck,
    title: 'Levering',
    description: 'Levering volgens uw specificaties. Op tijd, correct verpakt en gedocumenteerd.',
  },
]

export default function Process() {
  return (
    <section className="section-padding bg-graphite-900/50 relative overflow-hidden">
      {/* Subtle gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-graphite-950 via-transparent to-graphite-950" />

      <div className="container-industrial relative">
        {/* Section Header */}
        <AnimatedSection className="text-center max-w-3xl mx-auto mb-16 md:mb-24">
          <div className="flex items-center justify-center gap-4 mb-6">
            <div className="w-12 h-px bg-accent-500" />
            <span className="text-accent-400 font-mono text-mono uppercase tracking-widest">
              Werkwijze
            </span>
            <div className="w-12 h-px bg-accent-500" />
          </div>
          <h2 className="font-heading font-bold text-cream-50 text-heading-xl md:text-display mb-6">
            Zo gaan we te werk
          </h2>
          <p className="text-cream-300 text-body-lg">
            Een helder proces voor optimaal resultaat. Van tekening tot levering,
            wij denken mee bij elke stap.
          </p>
        </AnimatedSection>

        {/* Desktop: Horizontal Timeline */}
        <div className="hidden lg:block">
          <div className="relative">
            {/* Timeline Line */}
            <div className="absolute top-[60px] left-0 right-0 h-px bg-graphite-700">
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-accent-500/50 to-transparent" />
            </div>

            {/* Steps */}
            <div className="grid grid-cols-4 gap-8">
              {steps.map((step, index) => (
                <ProcessStep key={step.number} step={step} index={index} />
              ))}
            </div>
          </div>
        </div>

        {/* Mobile/Tablet: Vertical Timeline */}
        <div className="lg:hidden">
          <div className="relative pl-8 md:pl-12">
            {/* Vertical Timeline Line */}
            <div className="absolute left-0 top-0 bottom-0 w-px bg-graphite-700">
              <div className="absolute inset-0 bg-gradient-to-b from-accent-500/50 via-accent-500/30 to-transparent" />
            </div>

            {/* Steps */}
            <div className="space-y-12">
              {steps.map((step, index) => (
                <ProcessStepMobile key={step.number} step={step} index={index} />
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

interface ProcessStepProps {
  step: typeof steps[0]
  index: number
}

function ProcessStep({ step, index }: ProcessStepProps) {
  const Icon = step.icon

  return (
    <AnimatedSection delay={index * 150} className="relative pt-20">
      {/* Node */}
      <div className="absolute top-[52px] left-1/2 -translate-x-1/2 w-4 h-4 rounded-full bg-graphite-950 border-2 border-accent-500 z-10" />

      {/* Content */}
      <div className="text-center">
        {/* Step number */}
        <span className="inline-block font-mono text-accent-400 text-caption mb-4 tracking-wider">
          STAP {step.number}
        </span>

        {/* Icon */}
        <div className="w-16 h-16 mx-auto mb-6 flex items-center justify-center border border-graphite-600 bg-graphite-900/50">
          <Icon className="w-8 h-8 text-cream-300" />
        </div>

        {/* Title */}
        <h3 className="font-heading font-semibold text-cream-50 text-heading mb-3">
          {step.title}
        </h3>

        {/* Description */}
        <p className="text-cream-400 text-body-sm leading-relaxed">
          {step.description}
        </p>
      </div>
    </AnimatedSection>
  )
}

function ProcessStepMobile({ step, index }: ProcessStepProps) {
  const Icon = step.icon

  return (
    <AnimatedSection delay={index * 100} className="relative">
      {/* Node */}
      <div className="absolute -left-8 md:-left-12 top-0 w-3 h-3 rounded-full bg-graphite-950 border-2 border-accent-500 z-10" />

      {/* Content */}
      <div>
        {/* Step number & Icon row */}
        <div className="flex items-center gap-4 mb-4">
          <div className="w-12 h-12 flex items-center justify-center border border-graphite-600 bg-graphite-900/50">
            <Icon className="w-6 h-6 text-cream-300" />
          </div>
          <span className="font-mono text-accent-400 text-caption tracking-wider">
            STAP {step.number}
          </span>
        </div>

        {/* Title */}
        <h3 className="font-heading font-semibold text-cream-50 text-heading mb-2">
          {step.title}
        </h3>

        {/* Description */}
        <p className="text-cream-400 text-body-sm leading-relaxed">
          {step.description}
        </p>
      </div>
    </AnimatedSection>
  )
}
