import Hero from '@/components/sections/Hero'
import Capabilities from '@/components/sections/Capabilities'
import Process from '@/components/sections/Process'
import Metrics from '@/components/sections/Metrics'
import Testimonial from '@/components/sections/Testimonial'
import JobsTeaser from '@/components/sections/JobsTeaser'
import CTASection from '@/components/sections/CTASection'

export default function Home() {
  return (
    <>
      <Hero />
      <Capabilities />
      <Process />
      <Metrics />
      <JobsTeaser />
      <Testimonial />
      <CTASection />
    </>
  )
}
