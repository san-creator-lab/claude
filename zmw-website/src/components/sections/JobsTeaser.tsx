import { Link } from 'react-router-dom'
import {
  ChevronRight,
  Banknote,
  TrendingUp,
  CheckCircle,
  Sun
} from 'lucide-react'
import AnimatedSection from '../AnimatedSection'

const benefits = [
  {
    icon: Banknote,
    title: 'Goed salaris',
    description: 'Marktconform salaris met doorgroeimogelijkheden',
  },
  {
    icon: TrendingUp,
    title: 'Groei & Ontwikkeling',
    description: 'Opleidingsmogelijkheden en carrièreperspectief',
  },
  {
    icon: CheckCircle,
    title: 'Alles goed geregeld',
    description: 'Pensioenopbouw en andere secundaire arbeidsvoorwaarden',
  },
  {
    icon: Sun,
    title: 'Vakantiedagen',
    description: 'Ruime vakantieregeling',
  },
]

export default function JobsTeaser() {
  return (
    <section className="section-padding bg-graphite-950 relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 precision-grid opacity-20" />
      <div className="absolute top-0 left-1/4 w-1/2 h-1/2 bg-gradient-radial from-accent-500/5 to-transparent" />

      <div className="container-industrial relative">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">
          {/* Left Column - Content */}
          <AnimatedSection>
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-px bg-accent-500" />
              <span className="text-accent-400 font-mono text-mono uppercase tracking-widest">
                Vacatures
              </span>
            </div>

            <h2 className="font-heading font-bold text-cream-50 text-heading-xl md:text-display mb-6">
              Werken bij ZMW
            </h2>

            <p className="text-cream-300 text-body-lg mb-8">
              Werken in de draai & frees fabriek. Bij ZMW werk je met de nieuwste
              CNC-technologie in een modern machinepark. Een familiebedrijf met
              oog voor vakmanschap én voor jou.
            </p>

            {/* Benefits Grid */}
            <div className="grid grid-cols-2 gap-4 mb-10">
              {benefits.map((benefit, index) => (
                <AnimatedSection key={benefit.title} delay={index * 100}>
                  <div className="flex items-start gap-3 p-4 border border-graphite-700/50 bg-graphite-900/30 hover:border-accent-500/30 transition-colors">
                    <benefit.icon className="w-5 h-5 text-accent-400 mt-0.5 flex-shrink-0" />
                    <div>
                      <h4 className="font-heading font-semibold text-cream-100 text-body-sm mb-1">
                        {benefit.title}
                      </h4>
                      <p className="text-cream-400 text-caption leading-relaxed">
                        {benefit.description}
                      </p>
                    </div>
                  </div>
                </AnimatedSection>
              ))}
            </div>

            <Link to="/vacatures" className="btn-primary group">
              <span>Bekijk vacatures</span>
              <ChevronRight className="w-5 h-5 ml-2 transition-transform group-hover:translate-x-1" />
            </Link>
          </AnimatedSection>

          {/* Right Column - Visual */}
          <AnimatedSection delay={200}>
            <div className="relative">
              {/* Decorative frame */}
              <div className="absolute -inset-4 border border-graphite-700" />
              <div className="absolute -inset-8 border border-graphite-800/50" />

              {/* Image placeholder with industrial aesthetic */}
              <div className="relative aspect-[4/3] bg-gradient-to-br from-graphite-800 to-graphite-900 overflow-hidden">
                {/* Grid overlay */}
                <div className="absolute inset-0 precision-grid opacity-30" />

                {/* Content */}
                <div className="absolute inset-0 flex flex-col items-center justify-center p-8">
                  <div className="w-20 h-20 border-2 border-accent-500/50 rounded-full flex items-center justify-center mb-6">
                    <span className="font-heading font-bold text-accent-400 text-3xl">Z</span>
                  </div>
                  <span className="font-mono text-accent-400 text-mono uppercase tracking-widest mb-2">
                    Join Our Team
                  </span>
                  <span className="text-cream-300 text-center">
                    Moderne faciliteit • 35+ CNC-machines • Familiebedrijf
                  </span>
                </div>

                {/* Corner accents */}
                <div className="absolute top-4 left-4 w-8 h-8 border-l-2 border-t-2 border-accent-500" />
                <div className="absolute top-4 right-4 w-8 h-8 border-r-2 border-t-2 border-accent-500" />
                <div className="absolute bottom-4 left-4 w-8 h-8 border-l-2 border-b-2 border-accent-500" />
                <div className="absolute bottom-4 right-4 w-8 h-8 border-r-2 border-b-2 border-accent-500" />
              </div>
            </div>
          </AnimatedSection>
        </div>
      </div>
    </section>
  )
}
