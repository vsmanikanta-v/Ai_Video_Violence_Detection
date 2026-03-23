import { Link } from 'react-router-dom'
import { useAppSelector } from '@/store/hooks'
import { Layout } from '@/components/Layout'

const FEATURES = [
  'CNN + LSTM violence detection (inference-only)',
  'GenAI incident explanations (Gemini)',
  'JWT authentication & RBAC',
  'Video upload with progress & analysis history',
  'Audit logs & admin dashboard',
  'N-Tier: React, FastAPI, PostgreSQL',
]

const TECH_STACK = [
  { layer: 'Frontend', technology: 'React 19.2 · TypeScript · Tailwind CSS', purpose: 'Upload, results, history, admin UI' },
  { layer: 'Backend', technology: 'FastAPI · JWT · RBAC', purpose: 'REST API, auth, video & detection endpoints' },
  { layer: 'ML / GenAI', technology: 'CNN-LSTM stub · Google Gemini', purpose: 'Violence score, incident explanation' },
  { layer: 'Data', technology: 'PostgreSQL', purpose: 'Users, videos, results, audit_logs' },
]

function HeroSection() {
  return (
    <section className="text-center space-y-6 py-12">
      <h1 className="text-4xl sm:text-5xl font-bold text-soft-navy">
        AI Video Violence Detection
      </h1>
      <p className="text-soft-slate max-w-2xl mx-auto text-lg">
        Upload short video clips. Get violence detection scores, key timestamps, and
        human-readable incident explanations — all with a secure, auditable pipeline.
      </p>
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <Link
          to="/upload"
          className="bg-soft-sage/70 hover:bg-soft-sage text-soft-navy font-semibold px-8 py-3 rounded-lg transition shadow-sm"
        >
          Upload &amp; Analyse
        </Link>
        <Link
          to="/history"
          className="border-2 border-soft-sage/60 text-soft-navy hover:bg-soft-sage/20 font-semibold px-8 py-3 rounded-lg transition"
        >
          View History
        </Link>
      </div>
    </section>
  )
}

function ProblemSection() {
  return (
    <section className="max-w-4xl mx-auto py-10 text-center">
      <h2 className="text-2xl font-semibold text-soft-navy mb-4">What we solve</h2>
      <p className="text-soft-slate leading-relaxed">
        Surveillance and short-form video review is labour-intensive. This system runs
        violence detection (CNN-LSTM) on uploaded clips, then uses Generative AI to
        produce clear incident explanations. Results and audit trails are stored for
        compliance and review.
      </p>
    </section>
  )
}

function FeaturesSection() {
  return (
    <section className="py-10">
      <h2 className="text-2xl font-semibold text-soft-navy mb-6 text-center">Key features</h2>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 max-w-5xl mx-auto">
        {FEATURES.map((feature) => (
          <div
            key={feature}
            className="bg-white/80 rounded-xl border border-soft-sage/40 p-5 shadow-sm"
          >
            <p className="text-soft-navy font-medium">{feature}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

function TechStackSection() {
  return (
    <section className="max-w-4xl mx-auto py-10">
      <h2 className="text-2xl font-semibold text-soft-navy mb-6 text-center">Technology stack</h2>
      <div className="overflow-x-auto rounded-xl border border-soft-sage/40 shadow-sm">
        <table className="w-full text-sm text-left">
          <thead className="bg-soft-sand/60 text-soft-navy uppercase text-xs tracking-wide">
            <tr>
              <th scope="col" className="px-4 py-3">Layer</th>
              <th scope="col" className="px-4 py-3">Technology</th>
              <th scope="col" className="px-4 py-3">Purpose</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-soft-sage/20">
            {TECH_STACK.map(({ layer, technology, purpose }) => (
              <tr key={layer} className="bg-white/60 hover:bg-soft-sand/30">
                <td className="px-4 py-3 font-medium text-soft-navy">{layer}</td>
                <td className="px-4 py-3 text-soft-slate">{technology}</td>
                <td className="px-4 py-3 text-soft-slate">{purpose}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

function FooterCta() {
  return (
    <section className="py-12 text-center">
      <h2 className="text-2xl font-semibold text-soft-navy mb-2">Get started</h2>
      <p className="text-soft-slate mb-6 max-w-xl mx-auto">
        Create an account to upload videos and view detection results, or log in if you
        already have one.
      </p>
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <Link
          to="/register"
          className="bg-soft-sage/70 hover:bg-soft-sage text-soft-navy font-semibold px-8 py-3 rounded-lg transition"
        >
          Register
        </Link>
        <Link
          to="/login"
          className="border-2 border-soft-sage/60 text-soft-navy hover:bg-soft-sage/20 font-semibold px-8 py-3 rounded-lg transition"
        >
          Log in
        </Link>
      </div>
    </section>
  )
}

function LandingContent() {
  return (
    <>
      <HeroSection />
      <ProblemSection />
      <FeaturesSection />
      <TechStackSection />
      <FooterCta />
    </>
  )
}

function UnauthHeader() {
  return (
    <header className="sticky top-0 z-50 flex items-center justify-between px-4 sm:px-6 py-4 bg-soft-sand/80 border-b border-soft-sage/30 shadow-sm">
      <Link to="/" className="text-lg font-semibold text-soft-navy">
        AI Video Violence Detection
      </Link>
      <nav aria-label="Main navigation" className="flex items-center gap-3">
        <Link
          to="/login"
          className="border-2 border-soft-sage/60 text-soft-navy hover:bg-soft-sage/20 px-4 py-2 rounded-lg font-medium transition focus:outline-none focus:ring-2 focus:ring-soft-sage focus:ring-offset-2"
        >
          Log in
        </Link>
        <Link
          to="/register"
          className="bg-soft-sage/60 hover:bg-soft-sage text-soft-navy px-4 py-2 rounded-lg font-medium transition focus:outline-none focus:ring-2 focus:ring-soft-sage focus:ring-offset-2"
        >
          Register
        </Link>
      </nav>
    </header>
  )
}

/**
 * Landing page at /. Unauthenticated: full page with UnauthHeader + content.
 * Authenticated: same content inside Layout (nav shows Upload, History, Admin).
 */
export function LandingPage() {
  const token = useAppSelector((s) => s.auth.token)

  if (token) {
    return (
      <Layout>
        <LandingContent />
      </Layout>
    )
  }

  return (
    <div className="min-h-screen bg-soft-cream">
      <UnauthHeader />
      <main id="main-content" className="max-w-5xl mx-auto px-4 py-8 sm:py-12">
        <LandingContent />
      </main>
    </div>
  )
}
