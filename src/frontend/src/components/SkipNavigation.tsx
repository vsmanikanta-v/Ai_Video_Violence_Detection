export function SkipNavigation() {
  return (
    <a
      href="#main-content"
      className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-[100] focus:px-4 focus:py-2 focus:bg-soft-sage focus:text-soft-navy focus:rounded-lg focus:outline-none focus:ring-2 focus:ring-soft-sage focus:ring-offset-2 focus:font-medium"
    >
      Skip to main content
    </a>
  )
}
