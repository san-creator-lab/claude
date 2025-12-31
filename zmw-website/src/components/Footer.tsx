import { Link } from 'react-router-dom'
import { Phone, Mail, MapPin, Clock, Linkedin, ChevronRight } from 'lucide-react'
import Logo from './Logo'

export default function Footer() {
  return (
    <footer className="bg-graphite-950 border-t border-graphite-800/50">
      {/* Main Footer */}
      <div className="container-industrial py-16 md:py-20">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 lg:gap-8">
          {/* Brand Column */}
          <div className="lg:col-span-1">
            <Link to="/" className="flex items-center gap-3 mb-6">
              <Logo className="h-10 w-auto" />
              <div>
                <span className="block text-cream-100 font-heading font-bold text-lg tracking-tight">
                  ZMW
                </span>
                <span className="block text-cream-400 text-caption uppercase tracking-widest">
                  Draai & Freesfabriek
                </span>
              </div>
            </Link>
            <p className="text-cream-300 text-body-sm leading-relaxed mb-6">
              Sterk in CNC draaien & frezen. Van prototype tot serie, sinds 1960.
            </p>
            <div className="flex items-center gap-4">
              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 flex items-center justify-center border border-graphite-700 text-cream-300 hover:text-accent-400 hover:border-accent-500 transition-all"
                aria-label="LinkedIn"
              >
                <Linkedin className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="text-cream-100 font-heading font-semibold text-heading mb-6">
              Contact
            </h4>
            <ul className="space-y-4">
              <li>
                <a
                  href="tel:+31135436293"
                  className="flex items-start gap-3 text-cream-300 hover:text-accent-400 transition-colors group"
                >
                  <Phone className="w-5 h-5 mt-0.5 text-accent-500" />
                  <span>+31 13 543 62 93</span>
                </a>
              </li>
              <li>
                <a
                  href="mailto:info@zmwfabriek.nl"
                  className="flex items-start gap-3 text-cream-300 hover:text-accent-400 transition-colors group"
                >
                  <Mail className="w-5 h-5 mt-0.5 text-accent-500" />
                  <span>info@zmwfabriek.nl</span>
                </a>
              </li>
              <li>
                <div className="flex items-start gap-3 text-cream-300">
                  <MapPin className="w-5 h-5 mt-0.5 text-accent-500 flex-shrink-0" />
                  <span>
                    Calenwiel 25<br />
                    5056 DB Berkel-Enschot
                  </span>
                </div>
              </li>
              <li>
                <div className="flex items-start gap-3 text-cream-300">
                  <Clock className="w-5 h-5 mt-0.5 text-accent-500" />
                  <span>Ma - Vr: 07:00 - 17:00</span>
                </div>
              </li>
            </ul>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-cream-100 font-heading font-semibold text-heading mb-6">
              Navigatie
            </h4>
            <ul className="space-y-3">
              {[
                { name: 'Home', href: '/' },
                { name: 'Vacatures', href: '/vacatures' },
                { name: 'Contact', href: '/contact' },
              ].map((link) => (
                <li key={link.name}>
                  <Link
                    to={link.href}
                    className="text-cream-300 hover:text-accent-400 transition-colors inline-flex items-center gap-2 group"
                  >
                    <span>{link.name}</span>
                    <ChevronRight className="w-4 h-4 opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all" />
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* CTA Column */}
          <div>
            <h4 className="text-cream-100 font-heading font-semibold text-heading mb-6">
              Direct aan de slag
            </h4>
            <p className="text-cream-300 text-body-sm mb-6">
              Vraag vrijblijvend een offerte aan of neem contact met ons op om de mogelijkheden te bespreken.
            </p>
            <Link
              to="/contact"
              className="btn-primary w-full justify-center"
            >
              <span>Offerte aanvragen</span>
              <ChevronRight className="w-5 h-5 ml-2" />
            </Link>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-graphite-800/50">
        <div className="container-industrial py-6">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4 text-cream-400 text-body-sm">
            <p>
              © {new Date().getFullYear()} ZMW Draai & Freesfabriek. Alle rechten voorbehouden.
            </p>
            <p className="text-cream-500">
              Dé draai & frees fabriek, sinds 1960
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}
