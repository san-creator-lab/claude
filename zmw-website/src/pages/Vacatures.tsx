import { Link } from 'react-router-dom'
import {
  ChevronRight,
  MapPin,
  Clock,
  Banknote,
  TrendingUp,
  CheckCircle,
  Sun,
  Quote
} from 'lucide-react'
import { cn } from '@/lib/utils'
import AnimatedSection from '@/components/AnimatedSection'

const vacancies = [
  {
    slug: 'operationeel-manager',
    title: 'Operationeel Manager',
    subtitle: 'MT-lid',
    type: 'Fulltime',
    location: 'Berkel-Enschot',
    description: 'Ben jij sterk in organiseren, sturen en verbeteren? Krijg jij energie van het optimaliseren van processen en het aansturen van mensen? Dan zoeken we jou!',
    highlights: ['MT-lid', 'Leidinggevende rol', 'Procesoptimalisatie'],
  },
  {
    slug: 'cnc-langdraaier-programmeur',
    title: 'CNC Langdraaier & Programmeur',
    subtitle: 'Ervaren vakman',
    type: 'Fulltime',
    location: 'Berkel-Enschot',
    description: 'Voor ons moderne machinepark zoeken we een ervaren CNC Langdraaier die zelfstandig technische tekeningen kan lezen en omzetten naar programma\'s.',
    highlights: ['Zelfstandig werken', 'Moderne machines', 'Technisch uitdagend'],
  },
  {
    slug: 'open-sollicitatie',
    title: 'Open Sollicitatie',
    subtitle: 'Altijd welkom',
    type: 'Fulltime / Parttime',
    location: 'Berkel-Enschot',
    description: 'Staat er geen passende vacature bij? Neem dan toch contact op via het sollicitatieformulier. We kijken graag wat de mogelijkheden zijn.',
    highlights: ['Flexibele invulling', 'Kennismakingsgesprek', 'Kijk naar mogelijkheden'],
  },
]

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

export default function Vacatures() {
  return (
    <>
      {/* Hero */}
      <section className="relative pt-32 pb-20 md:pt-40 md:pb-28 overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0 bg-gradient-to-br from-graphite-950 via-graphite-900 to-graphite-950" />
        <div className="absolute inset-0 precision-grid opacity-30" />

        <div className="container-industrial relative">
          <AnimatedSection className="max-w-3xl">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-px bg-accent-500" />
              <span className="text-accent-400 font-mono text-mono uppercase tracking-widest">
                Vacatures
              </span>
            </div>
            <h1 className="font-heading font-bold text-cream-50 text-4xl md:text-display-lg mb-6">
              Werken in de draai & frees fabriek
            </h1>
            <p className="text-cream-300 text-lg md:text-xl">
              Bij ZMW werk je met de nieuwste CNC-technologie in een modern machinepark.
              Een familiebedrijf met oog voor vakmanschap én voor jou.
            </p>
          </AnimatedSection>
        </div>
      </section>

      {/* Vacancies */}
      <section className="section-padding bg-graphite-950">
        <div className="container-industrial">
          <div className="grid gap-6 lg:gap-8">
            {vacancies.map((vacancy, index) => (
              <VacancyCard key={vacancy.slug} vacancy={vacancy} index={index} />
            ))}
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section className="section-padding bg-graphite-900/50">
        <div className="absolute inset-0 bg-gradient-to-b from-graphite-950 via-transparent to-graphite-950" />

        <div className="container-industrial relative">
          <AnimatedSection className="text-center max-w-3xl mx-auto mb-16">
            <div className="flex items-center justify-center gap-4 mb-6">
              <div className="w-12 h-px bg-accent-500" />
              <span className="text-accent-400 font-mono text-mono uppercase tracking-widest">
                Arbeidsvoorwaarden
              </span>
              <div className="w-12 h-px bg-accent-500" />
            </div>
            <h2 className="font-heading font-bold text-cream-50 text-heading-xl md:text-display mb-6">
              Wat wij bieden
            </h2>
            <p className="text-cream-300 text-body-lg">
              Bij ZMW krijg je niet alleen een baan, maar een plek waar je jezelf kunt ontwikkelen.
            </p>
          </AnimatedSection>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {benefits.map((benefit, index) => (
              <AnimatedSection key={benefit.title} delay={index * 100}>
                <div className="card-industrial p-8 h-full text-center">
                  <div className="w-14 h-14 mx-auto mb-6 flex items-center justify-center border border-graphite-600">
                    <benefit.icon className="w-7 h-7 text-accent-400" />
                  </div>
                  <h3 className="font-heading font-semibold text-cream-100 text-heading mb-3">
                    {benefit.title}
                  </h3>
                  <p className="text-cream-400 text-body-sm">
                    {benefit.description}
                  </p>
                </div>
              </AnimatedSection>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonial */}
      <section className="section-padding bg-graphite-950">
        <div className="container-industrial">
          <div className="max-w-4xl mx-auto">
            <AnimatedSection className="text-center">
              <div className="flex justify-center mb-8">
                <div className="w-16 h-16 flex items-center justify-center border border-accent-500/50 bg-accent-500/10">
                  <Quote className="w-8 h-8 text-accent-400" />
                </div>
              </div>

              <blockquote className="mb-10">
                <p className="font-heading text-cream-100 text-xl md:text-2xl leading-relaxed font-medium">
                  "Nog steeds ga ik iedere dag met veel plezier naar mijn werk.
                  Ik ben begonnen op de afdeling nabewerking, om uiteindelijk door te groeien
                  naar de functie van machineprogrammeur voor onze automatische draai- en freesmachines.
                  Inmiddels ben ik alweer enkele jaren volwaardig CNC-Operator."
                </p>
              </blockquote>

              <div className="flex flex-col items-center">
                <div className="w-16 h-16 rounded-full bg-gradient-to-br from-accent-500 to-accent-600 flex items-center justify-center mb-4">
                  <span className="font-heading font-bold text-graphite-950 text-xl">R</span>
                </div>
                <cite className="not-italic">
                  <span className="block font-heading font-semibold text-cream-100 text-heading">
                    Rikkie
                  </span>
                  <span className="block text-cream-400 text-body-sm mt-1">
                    CNC-Operator bij ZMW
                  </span>
                </cite>
              </div>
            </AnimatedSection>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="section-padding bg-graphite-900/50">
        <div className="container-industrial">
          <AnimatedSection className="text-center max-w-2xl mx-auto">
            <h2 className="font-heading font-bold text-cream-50 text-heading-xl mb-6">
              Interesse?
            </h2>
            <p className="text-cream-300 text-body-lg mb-8">
              Neem contact op of solliciteer direct. We kijken graag samen naar de mogelijkheden.
            </p>
            <Link to="/contact" className="btn-primary">
              <span>Neem contact op</span>
              <ChevronRight className="w-5 h-5 ml-2" />
            </Link>
          </AnimatedSection>
        </div>
      </section>
    </>
  )
}

interface VacancyCardProps {
  vacancy: typeof vacancies[0]
  index: number
}

function VacancyCard({ vacancy, index }: VacancyCardProps) {
  return (
    <AnimatedSection delay={index * 100}>
      <Link
        to={`/vacatures/${vacancy.slug}`}
        className="block group"
      >
        <div className={cn(
          'card-industrial p-8 lg:p-10',
          'grid lg:grid-cols-[1fr,auto] gap-6 lg:gap-12 items-center'
        )}>
          {/* Content */}
          <div>
            {/* Meta */}
            <div className="flex flex-wrap items-center gap-4 mb-4">
              <span className="font-mono text-accent-400 text-caption uppercase tracking-wider">
                {vacancy.subtitle}
              </span>
              <div className="flex items-center gap-4 text-cream-400 text-body-sm">
                <span className="flex items-center gap-1.5">
                  <MapPin className="w-4 h-4" />
                  {vacancy.location}
                </span>
                <span className="flex items-center gap-1.5">
                  <Clock className="w-4 h-4" />
                  {vacancy.type}
                </span>
              </div>
            </div>

            {/* Title */}
            <h3 className="font-heading font-bold text-cream-50 text-heading-lg mb-3 group-hover:text-accent-400 transition-colors">
              {vacancy.title}
            </h3>

            {/* Description */}
            <p className="text-cream-300 text-body mb-4">
              {vacancy.description}
            </p>

            {/* Highlights */}
            <div className="flex flex-wrap gap-2">
              {vacancy.highlights.map((highlight) => (
                <span
                  key={highlight}
                  className="px-3 py-1 text-body-sm bg-graphite-800 text-cream-300 border border-graphite-700"
                >
                  {highlight}
                </span>
              ))}
            </div>
          </div>

          {/* Arrow */}
          <div className="hidden lg:flex items-center justify-center w-14 h-14 border border-graphite-600 group-hover:border-accent-500 group-hover:bg-accent-500/10 transition-all">
            <ChevronRight className="w-6 h-6 text-cream-300 group-hover:text-accent-400 transition-colors" />
          </div>
        </div>
      </Link>
    </AnimatedSection>
  )
}
