import { Link } from 'react-router-dom'
import { ChevronRight, Phone } from 'lucide-react'
import AnimatedSection from '../AnimatedSection'

export default function CTASection() {
  return (
    <section className="section-padding bg-graphite-950 relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 precision-grid opacity-20" />
      <div className="absolute inset-0 bg-gradient-to-r from-accent-500/5 via-transparent to-accent-500/5" />

      <div className="container-industrial relative">
        <AnimatedSection className="max-w-4xl mx-auto text-center">
          {/* Headline */}
          <h2 className="font-heading font-bold text-cream-50 text-heading-xl md:text-display mb-6">
            Klaar om te starten?
          </h2>
          <p className="text-cream-300 text-body-lg mb-10 max-w-2xl mx-auto">
            Vraag vrijblijvend een offerte aan of neem contact met ons op.
            We denken graag met u mee over de beste oplossing.
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/contact" className="btn-primary group">
              <span>Offerte aanvragen</span>
              <ChevronRight className="w-5 h-5 ml-2 transition-transform group-hover:translate-x-1" />
            </Link>
            <a
              href="tel:+31135436293"
              className="btn-secondary group"
            >
              <Phone className="w-5 h-5 mr-2" />
              <span>+31 13 543 62 93</span>
            </a>
          </div>

          {/* Trust note */}
          <p className="text-cream-500 text-body-sm mt-8">
            Geen verplichtingen • Snelle reactie • Persoonlijk advies
          </p>
        </AnimatedSection>
      </div>
    </section>
  )
}
