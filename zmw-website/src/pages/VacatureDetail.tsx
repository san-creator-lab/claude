import { useParams, Link } from 'react-router-dom'
import {
  ChevronLeft,
  ChevronRight,
  MapPin,
  Clock,
  Briefcase,
  CheckCircle,
  Mail,
  Phone
} from 'lucide-react'
import AnimatedSection from '@/components/AnimatedSection'

const vacancyData: Record<string, {
  title: string
  subtitle: string
  type: string
  location: string
  intro: string
  responsibilities: string[]
  requirements: string[]
  offer: string[]
}> = {
  'operationeel-manager': {
    title: 'Operationeel Manager',
    subtitle: 'MT-lid',
    type: 'Fulltime',
    location: 'Berkel-Enschot',
    intro: 'Ben jij sterk in organiseren, sturen en verbeteren? Krijg jij energie van het optimaliseren van processen en het aansturen van mensen? Dan zoeken we jou! Als Operationeel Manager ben je verantwoordelijk voor de dagelijkse aansturing van de productie en maak je deel uit van ons managementteam.',
    responsibilities: [
      'Dagelijkse aansturing van de productieafdeling',
      'Optimaliseren van productieprocessen',
      'Aansturen en coachen van medewerkers',
      'Bewaken van kwaliteit, doorlooptijden en kosten',
      'Deelname aan MT-vergaderingen en bijdragen aan strategische beslissingen',
      'Samenwerken met planning, inkoop en kwaliteit',
    ],
    requirements: [
      'HBO werk- en denkniveau',
      'Ervaring in een leidinggevende rol binnen productie/maakindustrie',
      'Sterk in organiseren en procesoptimalisatie',
      'Goede communicatieve vaardigheden',
      'Hands-on mentaliteit',
      'Kennis van CNC-verspaning is een pré',
    ],
    offer: [
      'Marktconform salaris',
      'Verantwoordelijke positie binnen MT',
      'Ruimte voor eigen inbreng en ontwikkeling',
      'Werken in modern machinepark',
      'Collegiale werksfeer in familiebedrijf',
      'Goede secundaire arbeidsvoorwaarden',
    ],
  },
  'cnc-langdraaier-programmeur': {
    title: 'CNC Langdraaier & Programmeur',
    subtitle: 'Ervaren vakman',
    type: 'Fulltime',
    location: 'Berkel-Enschot',
    intro: 'Voor ons moderne machinepark zoeken we een ervaren CNC Langdraaier die zelfstandig technische tekeningen kan lezen en omzetten naar programma\'s. Je werkt met de nieuwste technologie en hebt de ruimte om je vakmanschap verder te ontwikkelen.',
    responsibilities: [
      'Zelfstandig lezen en interpreteren van technische tekeningen',
      'Programmeren van CNC langdraaimachines',
      'Instellen en bedienen van machines',
      'Kwaliteitscontrole van geproduceerde onderdelen',
      'Bijdragen aan procesverbeteringen',
      'Onderhouden van machines volgens planning',
    ],
    requirements: [
      'MBO niveau 3/4 in richting verspaning of vergelijkbaar',
      'Ervaring met CNC langdraaien',
      'Zelfstandig technische tekeningen kunnen lezen',
      'Programmeerervaring (Fanuc/Siemens)',
      'Nauwkeurig en kwaliteitsbewust',
      'Zelfstandig kunnen werken',
    ],
    offer: [
      'Marktconform salaris op basis van ervaring',
      'Werken met moderne CNC-machines',
      'Opleidingsmogelijkheden',
      'Prettige werksfeer in familiebedrijf',
      'Goede secundaire arbeidsvoorwaarden',
      'Doorgroeimogelijkheden',
    ],
  },
  'open-sollicitatie': {
    title: 'Open Sollicitatie',
    subtitle: 'Altijd welkom',
    type: 'Fulltime / Parttime',
    location: 'Berkel-Enschot',
    intro: 'Staat er geen passende vacature bij? Neem dan toch contact op via het sollicitatieformulier. We kijken graag wat de mogelijkheden zijn. Bij ZMW zijn we altijd op zoek naar gemotiveerde mensen die passen bij ons team.',
    responsibilities: [
      'Afhankelijk van je achtergrond en interesses',
      'Mogelijk CNC-draaien of -frezen',
      'Mogelijk nabewerking of kwaliteitscontrole',
      'Mogelijk logistiek of planning',
      'We kijken samen naar wat past',
    ],
    requirements: [
      'Technische interesse of achtergrond',
      'Gemotiveerd en leergierig',
      'Teamspeler',
      'Betrouwbaar en nauwkeurig',
      'Goede beheersing Nederlandse taal',
    ],
    offer: [
      'Marktconform salaris',
      'Inwerken en opleidingsmogelijkheden',
      'Prettige werksfeer',
      'Modern machinepark',
      'Goede secundaire arbeidsvoorwaarden',
      'Echte aandacht voor medewerkers',
    ],
  },
}

export default function VacatureDetail() {
  const { slug } = useParams<{ slug: string }>()
  const vacancy = slug ? vacancyData[slug] : null

  if (!vacancy) {
    return (
      <section className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-cream-50 text-2xl mb-4">Vacature niet gevonden</h1>
          <Link to="/vacatures" className="btn-secondary">
            <ChevronLeft className="w-5 h-5 mr-2" />
            Terug naar vacatures
          </Link>
        </div>
      </section>
    )
  }

  return (
    <>
      {/* Hero */}
      <section className="relative pt-32 pb-16 md:pt-40 md:pb-20 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-graphite-950 via-graphite-900 to-graphite-950" />
        <div className="absolute inset-0 precision-grid opacity-30" />

        <div className="container-industrial relative">
          {/* Breadcrumb */}
          <AnimatedSection>
            <Link
              to="/vacatures"
              className="inline-flex items-center gap-2 text-cream-400 hover:text-accent-400 transition-colors mb-8"
            >
              <ChevronLeft className="w-4 h-4" />
              Alle vacatures
            </Link>
          </AnimatedSection>

          <AnimatedSection delay={100}>
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

            <h1 className="font-heading font-bold text-cream-50 text-4xl md:text-display mb-6">
              {vacancy.title}
            </h1>

            <p className="text-cream-300 text-lg md:text-xl max-w-3xl">
              {vacancy.intro}
            </p>
          </AnimatedSection>
        </div>
      </section>

      {/* Content */}
      <section className="section-padding bg-graphite-950">
        <div className="container-industrial">
          <div className="grid lg:grid-cols-3 gap-12 lg:gap-16">
            {/* Main Content */}
            <div className="lg:col-span-2 space-y-12">
              {/* Responsibilities */}
              <AnimatedSection>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 flex items-center justify-center border border-accent-500 bg-accent-500/10">
                    <Briefcase className="w-5 h-5 text-accent-400" />
                  </div>
                  <h2 className="font-heading font-bold text-cream-50 text-heading-lg">
                    Wat ga je doen?
                  </h2>
                </div>
                <ul className="space-y-3">
                  {vacancy.responsibilities.map((item, index) => (
                    <li key={index} className="flex items-start gap-3 text-cream-300">
                      <CheckCircle className="w-5 h-5 text-accent-500 mt-0.5 flex-shrink-0" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </AnimatedSection>

              {/* Requirements */}
              <AnimatedSection delay={100}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 flex items-center justify-center border border-accent-500 bg-accent-500/10">
                    <CheckCircle className="w-5 h-5 text-accent-400" />
                  </div>
                  <h2 className="font-heading font-bold text-cream-50 text-heading-lg">
                    Wat vragen wij?
                  </h2>
                </div>
                <ul className="space-y-3">
                  {vacancy.requirements.map((item, index) => (
                    <li key={index} className="flex items-start gap-3 text-cream-300">
                      <span className="w-1.5 h-1.5 rounded-full bg-accent-500 mt-2.5 flex-shrink-0" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </AnimatedSection>

              {/* Offer */}
              <AnimatedSection delay={200}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 flex items-center justify-center border border-accent-500 bg-accent-500/10">
                    <CheckCircle className="w-5 h-5 text-accent-400" />
                  </div>
                  <h2 className="font-heading font-bold text-cream-50 text-heading-lg">
                    Wat bieden wij?
                  </h2>
                </div>
                <ul className="space-y-3">
                  {vacancy.offer.map((item, index) => (
                    <li key={index} className="flex items-start gap-3 text-cream-300">
                      <CheckCircle className="w-5 h-5 text-accent-500 mt-0.5 flex-shrink-0" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </AnimatedSection>
            </div>

            {/* Sidebar */}
            <div className="lg:col-span-1">
              <AnimatedSection delay={300}>
                <div className="sticky top-28">
                  <div className="card-industrial p-8">
                    <h3 className="font-heading font-semibold text-cream-50 text-heading mb-6">
                      Interesse?
                    </h3>
                    <p className="text-cream-300 text-body-sm mb-6">
                      Solliciteer direct of neem contact op voor meer informatie.
                    </p>

                    <Link to="/contact" className="btn-primary w-full justify-center mb-4">
                      <span>Solliciteer nu</span>
                      <ChevronRight className="w-5 h-5 ml-2" />
                    </Link>

                    <div className="border-t border-graphite-700 pt-6 mt-6 space-y-4">
                      <a
                        href="tel:+31135436293"
                        className="flex items-center gap-3 text-cream-300 hover:text-accent-400 transition-colors"
                      >
                        <Phone className="w-5 h-5 text-accent-500" />
                        <span>+31 13 543 62 93</span>
                      </a>
                      <a
                        href="mailto:info@zmwfabriek.nl"
                        className="flex items-center gap-3 text-cream-300 hover:text-accent-400 transition-colors"
                      >
                        <Mail className="w-5 h-5 text-accent-500" />
                        <span>info@zmwfabriek.nl</span>
                      </a>
                    </div>
                  </div>
                </div>
              </AnimatedSection>
            </div>
          </div>
        </div>
      </section>

      {/* Other Vacancies */}
      <section className="section-padding bg-graphite-900/50">
        <div className="container-industrial">
          <AnimatedSection className="text-center mb-12">
            <h2 className="font-heading font-bold text-cream-50 text-heading-xl">
              Andere vacatures
            </h2>
          </AnimatedSection>

          <div className="flex justify-center">
            <Link
              to="/vacatures"
              className="btn-secondary"
            >
              <span>Bekijk alle vacatures</span>
              <ChevronRight className="w-5 h-5 ml-2" />
            </Link>
          </div>
        </div>
      </section>
    </>
  )
}
