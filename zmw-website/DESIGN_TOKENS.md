# ZMW Fabriek - Design Tokens & Component Library

## Design Language

Premium industrial-tech aesthetic inspired by Tesla, Apple, and Porsche.
- **Tesla**: Industrial aesthetics, high-tech confidence, "factory-grade"
- **Apple**: Minimalism, whitespace, premium typography, perfect details
- **Porsche**: Precision communication, sharp hierarchy, powerful CTAs

---

## Color Palette

### Primary: Graphite (Industrial Dark)
| Token | Hex | Usage |
|-------|-----|-------|
| `graphite-50` | `#f7f7f8` | Light backgrounds |
| `graphite-100` | `#eeeef0` | Subtle borders |
| `graphite-200` | `#d9d9de` | Disabled states |
| `graphite-700` | `#4c4c57` | Borders, dividers |
| `graphite-800` | `#41414a` | Card backgrounds |
| `graphite-900` | `#1a1a1f` | Section backgrounds |
| `graphite-950` | `#0d0d10` | Main background |

### Secondary: Cream (Typography/Space)
| Token | Hex | Usage |
|-------|-----|-------|
| `cream-50` | `#fefdfb` | Primary text (headings) |
| `cream-100` | `#fdfbf7` | Body text |
| `cream-200` | `#faf6ed` | Secondary text |
| `cream-300` | `#f5ede0` | Descriptions |
| `cream-400` | `#ede0cc` | Muted text |
| `cream-500` | `#e3d0b5` | Captions |

### Accent: Electric Cyan (Industrial Precision)
| Token | Hex | Usage |
|-------|-----|-------|
| `accent-400` | `#00e5f0` | Hover states, links |
| `accent-500` | `#00c8d4` | Primary CTA, icons |
| `accent-600` | `#00a0b2` | CTA hover |
| `accent-700` | `#007f8f` | Active states |

---

## Typography

### Font Families
- **Heading**: Inter (weight 600-700)
- **Body**: Inter (weight 400-500)
- **Mono**: JetBrains Mono (for data/specs/tolerances)

### Scale
| Token | Size | Line Height | Weight | Usage |
|-------|------|-------------|--------|-------|
| `display-xl` | 5rem | 1 | 700 | Hero headlines |
| `display-lg` | 3.75rem | 1.05 | 700 | Page titles |
| `display` | 3rem | 1.1 | 700 | Section headers |
| `heading-xl` | 2.25rem | 1.15 | 600 | Large headings |
| `heading-lg` | 1.875rem | 1.2 | 600 | Card titles |
| `heading` | 1.5rem | 1.25 | 600 | Subsections |
| `body-lg` | 1.125rem | 1.6 | 400 | Lead paragraphs |
| `body` | 1rem | 1.6 | 400 | Body text |
| `body-sm` | 0.875rem | 1.5 | 400 | Small text |
| `caption` | 0.75rem | 1.4 | 500 | Labels, captions |
| `mono` | 0.875rem | 1.4 | 500 | Data, specs |

---

## Spacing

### Base Scale
- Large margins: `px-6 md:px-12 lg:px-20`
- Section padding: `py-20 md:py-28 lg:py-36`
- Container max-width: `max-w-8xl` (88rem)

### Grid
- 12-column grid with large gutters
- Sharp alignment
- Generous whitespace

---

## Components

### Buttons

#### Primary CTA (`.btn-primary`)
```css
bg-accent-500 text-graphite-950 font-semibold
hover:bg-accent-400 hover:translate-y-[-2px]
```

#### Secondary CTA (`.btn-secondary`)
```css
border-2 border-cream-200 text-cream-100
hover:bg-cream-100 hover:text-graphite-950
```

#### Ghost Button (`.btn-ghost`)
```css
text-cream-200 hover:text-accent-400
gap-2 hover:gap-3 (arrow animation)
```

### Cards (`.card-industrial`)
```css
bg-graphite-900/50 backdrop-blur-sm
border border-graphite-700/50
hover:border-accent-500/50 hover:translate-y-[-4px]
```

### Industrial Line (`.industrial-line`)
```css
::before { left: 0; width: 1px; bg-accent-500; }
```

---

## Animations & Interactions

### Scroll Animations
- **fade-up**: opacity 0→1, translateY 30px→0
- **slide-left**: opacity 0→1, translateX -30px→0
- **scale-in**: opacity 0→1, scale 0.95→1

### Micro-interactions
- Hover lift on cards: `translate-y-[-4px]`
- Button arrow shift: `translate-x-1` on hover
- Counter animations: 2s ease-out number counting
- Subtle parallax on images

### Timing
- Fast transitions: `duration-300`
- Medium transitions: `duration-500`
- Slow transitions: `duration-700`
- Easing: `ease-out`

---

## Page Structure

### Home
1. Hero (full-bleed, dark gradient)
2. Capabilities (6 cards)
3. Process (4-step timeline)
4. Metrics (spec-sheet style)
5. Jobs Teaser
6. Testimonial
7. CTA Section

### Vacatures
1. Hero
2. Vacancy Cards
3. Benefits Grid
4. Testimonial
5. CTA

### Contact
1. Hero
2. Split Layout (info + form)
3. Bottom CTA

---

## Hidden/Removed Pages

The following demo/template pages should be hidden or removed:
- `/blog` - Not relevant
- `/portfolio` - Not relevant
- `/case-studies` - Not relevant
- Any other theme demo content

---

## Responsive Breakpoints

| Breakpoint | Width |
|------------|-------|
| `sm` | 640px |
| `md` | 768px |
| `lg` | 1024px |
| `xl` | 1280px |
| `2xl` | 1536px |

---

## Accessibility

- Contrast ratio: AAA for body text, AA for large text
- Focus states: `ring-2 ring-accent-400 ring-offset-2`
- Keyboard navigation: Full support
- Screen reader: Proper ARIA labels
