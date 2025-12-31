import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu, X, ChevronRight } from 'lucide-react'
import { cn } from '@/lib/utils'
import Logo from './Logo'

const navItems = [
  { name: 'Home', href: '/' },
  { name: 'Vacatures', href: '/vacatures' },
  { name: 'Contact', href: '/contact' },
]

export default function Navigation() {
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const location = useLocation()

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  useEffect(() => {
    setIsMobileMenuOpen(false)
  }, [location])

  return (
    <>
      <header
        className={cn(
          'fixed top-0 left-0 right-0 z-50 transition-all duration-500',
          isScrolled
            ? 'bg-graphite-950/95 backdrop-blur-md border-b border-graphite-800/50'
            : 'bg-transparent'
        )}
      >
        <div className="container-industrial">
          <nav className="flex items-center justify-between h-20 md:h-24">
            {/* Logo */}
            <Link
              to="/"
              className="relative z-10 flex items-center gap-3 group"
            >
              <Logo className="h-10 w-auto" />
              <div className="hidden sm:block">
                <span className="block text-cream-100 font-heading font-bold text-lg tracking-tight">
                  ZMW
                </span>
                <span className="block text-cream-400 text-caption uppercase tracking-widest">
                  Draai & Freesfabriek
                </span>
              </div>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-12">
              {navItems.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className={cn(
                    'relative text-body font-medium transition-colors duration-300',
                    location.pathname === item.href
                      ? 'text-accent-400'
                      : 'text-cream-200 hover:text-cream-50'
                  )}
                >
                  {item.name}
                  {location.pathname === item.href && (
                    <span className="absolute -bottom-1 left-0 w-full h-0.5 bg-accent-500" />
                  )}
                </Link>
              ))}
            </div>

            {/* Desktop CTA */}
            <div className="hidden md:block">
              <Link
                to="/contact"
                className="btn-primary group"
              >
                <span>Offerte aanvragen</span>
                <ChevronRight className="w-5 h-5 ml-2 transition-transform group-hover:translate-x-1" />
              </Link>
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="md:hidden relative z-10 p-2 text-cream-100 hover:text-accent-400 transition-colors"
              aria-label="Toggle menu"
            >
              {isMobileMenuOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </button>
          </nav>
        </div>
      </header>

      {/* Mobile Menu */}
      <div
        className={cn(
          'fixed inset-0 z-40 md:hidden transition-all duration-500',
          isMobileMenuOpen
            ? 'opacity-100 pointer-events-auto'
            : 'opacity-0 pointer-events-none'
        )}
      >
        {/* Backdrop */}
        <div
          className="absolute inset-0 bg-graphite-950/98 backdrop-blur-lg"
          onClick={() => setIsMobileMenuOpen(false)}
        />

        {/* Menu Content */}
        <div className="relative h-full flex flex-col justify-center px-6">
          <nav className="space-y-2">
            {navItems.map((item, index) => (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  'block text-display font-heading font-bold transition-all duration-300',
                  'transform',
                  isMobileMenuOpen
                    ? 'translate-x-0 opacity-100'
                    : '-translate-x-8 opacity-0',
                  location.pathname === item.href
                    ? 'text-accent-400'
                    : 'text-cream-100 hover:text-accent-300'
                )}
                style={{ transitionDelay: `${index * 100 + 200}ms` }}
              >
                {item.name}
              </Link>
            ))}
          </nav>

          <div
            className={cn(
              'mt-12 transition-all duration-500',
              isMobileMenuOpen
                ? 'translate-y-0 opacity-100'
                : 'translate-y-4 opacity-0'
            )}
            style={{ transitionDelay: '500ms' }}
          >
            <Link
              to="/contact"
              className="btn-primary w-full justify-center"
            >
              <span>Offerte aanvragen</span>
              <ChevronRight className="w-5 h-5 ml-2" />
            </Link>
          </div>

          {/* Contact Info */}
          <div
            className={cn(
              'absolute bottom-12 left-6 right-6 transition-all duration-500',
              isMobileMenuOpen
                ? 'translate-y-0 opacity-100'
                : 'translate-y-4 opacity-0'
            )}
            style={{ transitionDelay: '600ms' }}
          >
            <div className="border-t border-graphite-700 pt-6">
              <a
                href="tel:+31135436293"
                className="block text-cream-300 hover:text-accent-400 transition-colors"
              >
                +31 13 543 62 93
              </a>
              <a
                href="mailto:info@zmwfabriek.nl"
                className="block text-cream-300 hover:text-accent-400 transition-colors mt-1"
              >
                info@zmwfabriek.nl
              </a>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
