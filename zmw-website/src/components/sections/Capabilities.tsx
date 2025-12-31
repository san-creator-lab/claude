import { useState } from 'react'
import {
  Cog,
  Layers,
  Paintbrush,
  Scissors,
  Wrench,
  Truck,
  ChevronRight
} from 'lucide-react'
import { cn } from '@/lib/utils'
import AnimatedSection from '../AnimatedSection'

const capabilities = [
  {
    id: 'prototyping',
    icon: Cog,
    title: 'Prototyping & Enkelstuks',
    description: 'Van prototype en enkeldelen tot kleine series. Snel schakelen, flexibel meedenken.',
    benefit: 'Snelle doorlooptijd, flexibele aanpak',
  },
  {
    id: 'series',
    icon: Layers,
    title: 'Seriematig 250-100.000+',
    description: 'Grote series met constante kwaliteit. Onbemande productie met ons high-end CNC machinepark.',
    benefit: 'Constante kwaliteit, concurrerende prijzen',
  },
  {
    id: 'surface',
    icon: Paintbrush,
    title: 'Oppervlaktebehandelingen',
    description: 'Passiveren, galvaniseren, coaten en andere nabehandelingen. Alles onder één dak geregeld.',
    benefit: 'Totaaloplossing, één aanspreekpunt',
  },
  {
    id: 'laser',
    icon: Scissors,
    title: 'Lasersnijden & Zetwerk',
    description: 'Lasersnijden en zetten als productiestappen richting het eindproduct.',
    benefit: 'Complete productieketen in-house',
  },
  {
    id: 'assembly',
    icon: Wrench,
    title: 'Assembleren & Samenstellen',
    description: 'Door onze hoge mate van precisie kunnen we CNC-gedraaide/freesproducten in eigen fabriek assembleren.',
    benefit: 'Kant-en-klare componenten geleverd',
  },
  {
    id: 'transport',
    icon: Truck,
    title: 'Transport & Logistiek',
    description: 'Produceren met een uitermate hoge kwaliteit, grotendeels onbemand CNC machinepark. Kwaliteit is geen belofte maar een logisch gevolg.',
    benefit: 'Betrouwbare levering, op maat',
  },
]

export default function Capabilities() {
  return (
    <section className="section-padding bg-graphite-950 relative overflow-hidden">
      {/* Background elements */}
      <div className="absolute inset-0 precision-grid opacity-20" />
      <div className="absolute top-0 right-0 w-1/2 h-1/2 bg-gradient-radial from-accent-500/5 to-transparent" />

      <div className="container-industrial relative">
        {/* Section Header */}
        <AnimatedSection className="max-w-3xl mb-16 md:mb-20">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-12 h-px bg-accent-500" />
            <span className="text-accent-400 font-mono text-mono uppercase tracking-widest">
              Wat we doen
            </span>
          </div>
          <h2 className="font-heading font-bold text-cream-50 text-heading-xl md:text-display mb-6">
            Alles onder één dak
          </h2>
          <p className="text-cream-300 text-body-lg">
            Van enkelstuks tot grote series. Alle gangbare staalsoorten, RVS, messing,
            aluminium en kunststof. Met meer dan 35 CNC draai- en freesmachines.
          </p>
        </AnimatedSection>

        {/* Capabilities Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {capabilities.map((capability, index) => (
            <CapabilityCard
              key={capability.id}
              capability={capability}
              index={index}
            />
          ))}
        </div>
      </div>
    </section>
  )
}

interface CapabilityCardProps {
  capability: typeof capabilities[0]
  index: number
}

function CapabilityCard({ capability, index }: CapabilityCardProps) {
  const [isHovered, setIsHovered] = useState(false)
  const Icon = capability.icon

  return (
    <AnimatedSection
      delay={index * 100}
      className="h-full"
    >
      <div
        className={cn(
          'card-industrial h-full p-8 cursor-pointer group',
          'flex flex-col'
        )}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        {/* Icon */}
        <div className="mb-6">
          <div className={cn(
            'w-14 h-14 flex items-center justify-center',
            'border border-graphite-600 group-hover:border-accent-500',
            'transition-all duration-300'
          )}>
            <Icon className={cn(
              'w-7 h-7 transition-colors duration-300',
              isHovered ? 'text-accent-400' : 'text-cream-300'
            )} />
          </div>
        </div>

        {/* Content */}
        <h3 className="font-heading font-semibold text-cream-50 text-heading mb-3">
          {capability.title}
        </h3>
        <p className="text-cream-400 text-body-sm leading-relaxed flex-1">
          {capability.description}
        </p>

        {/* Benefit reveal on hover */}
        <div className={cn(
          'mt-6 pt-6 border-t border-graphite-700',
          'transition-all duration-300',
          isHovered ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'
        )}>
          <div className="flex items-center gap-2 text-accent-400 text-body-sm font-medium">
            <ChevronRight className="w-4 h-4" />
            <span>{capability.benefit}</span>
          </div>
        </div>
      </div>
    </AnimatedSection>
  )
}
