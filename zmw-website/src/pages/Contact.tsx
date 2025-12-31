import { useState, FormEvent } from 'react'
import {
  Phone,
  Mail,
  MapPin,
  Clock,
  Upload,
  CheckCircle,
  ChevronRight,
  Send
} from 'lucide-react'
import { cn } from '@/lib/utils'
import AnimatedSection from '@/components/AnimatedSection'

type RequestType = 'freeswerk' | 'draaiwerk' | 'anders' | 'advies' | ''

export default function Contact() {
  const [requestType, setRequestType] = useState<RequestType>('')
  const [fileName, setFileName] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFileName(e.target.files[0].name)
    }
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    // Simulate form submission
    await new Promise(resolve => setTimeout(resolve, 1500))

    setIsSubmitting(false)
    setIsSubmitted(true)
  }

  return (
    <>
      {/* Hero */}
      <section className="relative pt-32 pb-16 md:pt-40 md:pb-20 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-graphite-950 via-graphite-900 to-graphite-950" />
        <div className="absolute inset-0 precision-grid opacity-30" />

        <div className="container-industrial relative">
          <AnimatedSection className="max-w-3xl">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-px bg-accent-500" />
              <span className="text-accent-400 font-mono text-mono uppercase tracking-widest">
                Contact
              </span>
            </div>
            <h1 className="font-heading font-bold text-cream-50 text-4xl md:text-display-lg mb-6">
              Neem contact op
            </h1>
            <p className="text-cream-300 text-lg md:text-xl">
              Vraag vrijblijvend een offerte aan of neem contact met ons op.
              We denken graag met u mee over de beste oplossing.
            </p>
          </AnimatedSection>
        </div>
      </section>

      {/* Contact Section */}
      <section className="section-padding bg-graphite-950">
        <div className="container-industrial">
          <div className="grid lg:grid-cols-2 gap-12 lg:gap-20">
            {/* Left: Contact Info */}
            <AnimatedSection>
              <div className="space-y-8">
                <div>
                  <h2 className="font-heading font-bold text-cream-50 text-heading-lg mb-6">
                    Contactgegevens
                  </h2>

                  <div className="space-y-6">
                    <a
                      href="tel:+31135436293"
                      className="flex items-start gap-4 group"
                    >
                      <div className="w-12 h-12 flex items-center justify-center border border-graphite-600 group-hover:border-accent-500 transition-colors">
                        <Phone className="w-6 h-6 text-accent-500" />
                      </div>
                      <div>
                        <span className="block text-cream-400 text-body-sm mb-1">Telefoon</span>
                        <span className="block text-cream-100 text-body-lg group-hover:text-accent-400 transition-colors">
                          +31 13 543 62 93
                        </span>
                      </div>
                    </a>

                    <a
                      href="mailto:info@zmwfabriek.nl"
                      className="flex items-start gap-4 group"
                    >
                      <div className="w-12 h-12 flex items-center justify-center border border-graphite-600 group-hover:border-accent-500 transition-colors">
                        <Mail className="w-6 h-6 text-accent-500" />
                      </div>
                      <div>
                        <span className="block text-cream-400 text-body-sm mb-1">E-mail</span>
                        <span className="block text-cream-100 text-body-lg group-hover:text-accent-400 transition-colors">
                          info@zmwfabriek.nl
                        </span>
                      </div>
                    </a>

                    <div className="flex items-start gap-4">
                      <div className="w-12 h-12 flex items-center justify-center border border-graphite-600">
                        <MapPin className="w-6 h-6 text-accent-500" />
                      </div>
                      <div>
                        <span className="block text-cream-400 text-body-sm mb-1">Adres</span>
                        <span className="block text-cream-100 text-body-lg">
                          Calenwiel 25<br />
                          5056 DB Berkel-Enschot
                        </span>
                      </div>
                    </div>

                    <div className="flex items-start gap-4">
                      <div className="w-12 h-12 flex items-center justify-center border border-graphite-600">
                        <Clock className="w-6 h-6 text-accent-500" />
                      </div>
                      <div>
                        <span className="block text-cream-400 text-body-sm mb-1">Openingstijden</span>
                        <span className="block text-cream-100 text-body-lg">
                          Maandag - Vrijdag<br />
                          07:00 - 17:00
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Map placeholder */}
                <div className="relative aspect-[4/3] bg-graphite-900 border border-graphite-700 overflow-hidden">
                  <div className="absolute inset-0 precision-grid opacity-30" />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="text-center">
                      <MapPin className="w-12 h-12 text-accent-500 mx-auto mb-4" />
                      <span className="block text-cream-300 mb-2">Calenwiel 25</span>
                      <span className="block text-cream-400 text-body-sm">Berkel-Enschot</span>
                    </div>
                  </div>
                  {/* Corner accents */}
                  <div className="absolute top-4 left-4 w-6 h-6 border-l-2 border-t-2 border-accent-500" />
                  <div className="absolute top-4 right-4 w-6 h-6 border-r-2 border-t-2 border-accent-500" />
                  <div className="absolute bottom-4 left-4 w-6 h-6 border-l-2 border-b-2 border-accent-500" />
                  <div className="absolute bottom-4 right-4 w-6 h-6 border-r-2 border-b-2 border-accent-500" />
                </div>
              </div>
            </AnimatedSection>

            {/* Right: Form */}
            <AnimatedSection delay={200}>
              <div className="card-industrial p-8 lg:p-10">
                {isSubmitted ? (
                  <div className="text-center py-12">
                    <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-accent-500/20 flex items-center justify-center">
                      <CheckCircle className="w-10 h-10 text-accent-400" />
                    </div>
                    <h3 className="font-heading font-bold text-cream-50 text-heading-lg mb-4">
                      Bericht verzonden
                    </h3>
                    <p className="text-cream-300 mb-8">
                      Bedankt voor uw bericht. We nemen zo spoedig mogelijk contact met u op.
                    </p>
                    <button
                      onClick={() => setIsSubmitted(false)}
                      className="btn-secondary"
                    >
                      Nieuw bericht versturen
                    </button>
                  </div>
                ) : (
                  <>
                    <h2 className="font-heading font-bold text-cream-50 text-heading-lg mb-2">
                      Offerte aanvragen
                    </h2>
                    <p className="text-cream-400 text-body-sm mb-8">
                      Vul het formulier in en we nemen zo spoedig mogelijk contact op.
                    </p>

                    <form onSubmit={handleSubmit} className="space-y-6">
                      {/* Request Type */}
                      <div>
                        <label className="block text-cream-200 text-body-sm font-medium mb-3">
                          Type aanvraag
                        </label>
                        <div className="grid grid-cols-2 gap-3">
                          {[
                            { value: 'freeswerk', label: 'Freeswerk' },
                            { value: 'draaiwerk', label: 'Draaiwerk' },
                            { value: 'anders', label: 'Anders' },
                            { value: 'advies', label: 'Graag advies' },
                          ].map((type) => (
                            <button
                              key={type.value}
                              type="button"
                              onClick={() => setRequestType(type.value as RequestType)}
                              className={cn(
                                'p-4 text-left border transition-all duration-300',
                                requestType === type.value
                                  ? 'border-accent-500 bg-accent-500/10 text-cream-100'
                                  : 'border-graphite-600 bg-graphite-800/50 text-cream-300 hover:border-graphite-500'
                              )}
                            >
                              <span className="text-body-sm font-medium">{type.label}</span>
                            </button>
                          ))}
                        </div>
                      </div>

                      {/* Name & Company */}
                      <div className="grid sm:grid-cols-2 gap-4">
                        <div>
                          <label htmlFor="name" className="block text-cream-200 text-body-sm font-medium mb-2">
                            Naam *
                          </label>
                          <input
                            type="text"
                            id="name"
                            required
                            className="w-full px-4 py-3 bg-graphite-800 border border-graphite-600 text-cream-100 placeholder-cream-500 focus:border-accent-500 focus:outline-none transition-colors"
                            placeholder="Uw naam"
                          />
                        </div>
                        <div>
                          <label htmlFor="company" className="block text-cream-200 text-body-sm font-medium mb-2">
                            Bedrijf
                          </label>
                          <input
                            type="text"
                            id="company"
                            className="w-full px-4 py-3 bg-graphite-800 border border-graphite-600 text-cream-100 placeholder-cream-500 focus:border-accent-500 focus:outline-none transition-colors"
                            placeholder="Uw bedrijf"
                          />
                        </div>
                      </div>

                      {/* Email & Phone */}
                      <div className="grid sm:grid-cols-2 gap-4">
                        <div>
                          <label htmlFor="email" className="block text-cream-200 text-body-sm font-medium mb-2">
                            E-mail *
                          </label>
                          <input
                            type="email"
                            id="email"
                            required
                            className="w-full px-4 py-3 bg-graphite-800 border border-graphite-600 text-cream-100 placeholder-cream-500 focus:border-accent-500 focus:outline-none transition-colors"
                            placeholder="uw@email.nl"
                          />
                        </div>
                        <div>
                          <label htmlFor="phone" className="block text-cream-200 text-body-sm font-medium mb-2">
                            Telefoon
                          </label>
                          <input
                            type="tel"
                            id="phone"
                            className="w-full px-4 py-3 bg-graphite-800 border border-graphite-600 text-cream-100 placeholder-cream-500 focus:border-accent-500 focus:outline-none transition-colors"
                            placeholder="+31 6 12345678"
                          />
                        </div>
                      </div>

                      {/* File Upload */}
                      <div>
                        <label className="block text-cream-200 text-body-sm font-medium mb-2">
                          Tekening uploaden
                        </label>
                        <label
                          className={cn(
                            'flex items-center justify-center gap-3 p-6 border-2 border-dashed cursor-pointer transition-colors',
                            fileName
                              ? 'border-accent-500 bg-accent-500/10'
                              : 'border-graphite-600 hover:border-graphite-500'
                          )}
                        >
                          <input
                            type="file"
                            className="hidden"
                            accept=".pdf,.step,.stp,.dxf,.dwg,.png,.jpg"
                            onChange={handleFileChange}
                          />
                          {fileName ? (
                            <>
                              <CheckCircle className="w-5 h-5 text-accent-400" />
                              <span className="text-cream-100 text-body-sm">{fileName}</span>
                            </>
                          ) : (
                            <>
                              <Upload className="w-5 h-5 text-cream-400" />
                              <span className="text-cream-400 text-body-sm">
                                PDF, STEP, DXF, DWG of afbeelding
                              </span>
                            </>
                          )}
                        </label>
                      </div>

                      {/* Message */}
                      <div>
                        <label htmlFor="message" className="block text-cream-200 text-body-sm font-medium mb-2">
                          Projectomschrijving *
                        </label>
                        <textarea
                          id="message"
                          required
                          rows={5}
                          className="w-full px-4 py-3 bg-graphite-800 border border-graphite-600 text-cream-100 placeholder-cream-500 focus:border-accent-500 focus:outline-none transition-colors resize-none"
                          placeholder="Beschrijf uw project, gewenste aantallen, materiaal, etc."
                        />
                      </div>

                      {/* Submit */}
                      <button
                        type="submit"
                        disabled={isSubmitting}
                        className={cn(
                          'btn-primary w-full justify-center',
                          isSubmitting && 'opacity-75 cursor-not-allowed'
                        )}
                      >
                        {isSubmitting ? (
                          <>
                            <svg className="animate-spin w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                            </svg>
                            <span>Verzenden...</span>
                          </>
                        ) : (
                          <>
                            <span>Verstuur aanvraag</span>
                            <Send className="w-5 h-5 ml-2" />
                          </>
                        )}
                      </button>
                    </form>
                  </>
                )}
              </div>
            </AnimatedSection>
          </div>
        </div>
      </section>

      {/* Bottom CTA */}
      <section className="py-16 bg-graphite-900/50">
        <div className="container-industrial">
          <AnimatedSection className="text-center">
            <p className="text-cream-300 text-body-lg mb-6">
              Liever direct bellen?
            </p>
            <a
              href="tel:+31135436293"
              className="btn-secondary group inline-flex"
            >
              <Phone className="w-5 h-5 mr-2" />
              <span>+31 13 543 62 93</span>
              <ChevronRight className="w-5 h-5 ml-2 opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all" />
            </a>
          </AnimatedSection>
        </div>
      </section>
    </>
  )
}
