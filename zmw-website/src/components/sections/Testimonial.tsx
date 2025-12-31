import { Quote } from 'lucide-react'
import AnimatedSection from '../AnimatedSection'

export default function Testimonial() {
  return (
    <section className="section-padding bg-graphite-900/50 relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-graphite-950 via-transparent to-graphite-950" />
      <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1/3 h-px bg-gradient-to-r from-transparent via-accent-500/30 to-transparent" />
      <div className="absolute right-0 top-1/2 -translate-y-1/2 w-1/3 h-px bg-gradient-to-l from-transparent via-accent-500/30 to-transparent" />

      <div className="container-industrial relative">
        <div className="max-w-4xl mx-auto">
          <AnimatedSection className="text-center">
            {/* Quote Icon */}
            <div className="flex justify-center mb-8">
              <div className="w-16 h-16 flex items-center justify-center border border-accent-500/50 bg-accent-500/10">
                <Quote className="w-8 h-8 text-accent-400" />
              </div>
            </div>

            {/* Quote */}
            <blockquote className="mb-10">
              <p className="font-heading text-cream-100 text-xl md:text-2xl lg:text-3xl leading-relaxed font-medium">
                "Nog steeds ga ik iedere dag met veel plezier naar mijn werk.
                Ik ben begonnen op de afdeling nabewerking, om uiteindelijk door te groeien
                naar de functie van machineprogrammeur voor onze automatische draai- en freesmachines.
                Inmiddels ben ik alweer enkele jaren volwaardig CNC-Operator."
              </p>
            </blockquote>

            {/* Author */}
            <div className="flex flex-col items-center">
              {/* Avatar placeholder */}
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
  )
}
