import { cn } from '@/lib/utils'

interface LogoProps {
  className?: string
}

export default function Logo({ className }: LogoProps) {
  return (
    <svg
      viewBox="0 0 48 48"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={cn('text-accent-500', className)}
    >
      {/* Precision gear/cog representing CNC machinery */}
      <circle
        cx="24"
        cy="24"
        r="20"
        stroke="currentColor"
        strokeWidth="2"
        fill="none"
        opacity="0.3"
      />
      <circle
        cx="24"
        cy="24"
        r="12"
        stroke="currentColor"
        strokeWidth="2"
        fill="none"
      />
      {/* Center precision point */}
      <circle
        cx="24"
        cy="24"
        r="3"
        fill="currentColor"
      />
      {/* Precision crosshairs */}
      <line
        x1="24"
        y1="4"
        x2="24"
        y2="12"
        stroke="currentColor"
        strokeWidth="2"
      />
      <line
        x1="24"
        y1="36"
        x2="24"
        y2="44"
        stroke="currentColor"
        strokeWidth="2"
      />
      <line
        x1="4"
        y1="24"
        x2="12"
        y2="24"
        stroke="currentColor"
        strokeWidth="2"
      />
      <line
        x1="36"
        y1="24"
        x2="44"
        y2="24"
        stroke="currentColor"
        strokeWidth="2"
      />
      {/* Diagonal precision markers */}
      <line
        x1="9.86"
        y1="9.86"
        x2="15.51"
        y2="15.51"
        stroke="currentColor"
        strokeWidth="1.5"
        opacity="0.6"
      />
      <line
        x1="32.49"
        y1="32.49"
        x2="38.14"
        y2="38.14"
        stroke="currentColor"
        strokeWidth="1.5"
        opacity="0.6"
      />
      <line
        x1="38.14"
        y1="9.86"
        x2="32.49"
        y2="15.51"
        stroke="currentColor"
        strokeWidth="1.5"
        opacity="0.6"
      />
      <line
        x1="15.51"
        y1="32.49"
        x2="9.86"
        y2="38.14"
        stroke="currentColor"
        strokeWidth="1.5"
        opacity="0.6"
      />
    </svg>
  )
}
