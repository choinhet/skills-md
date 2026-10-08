const BAR_WIDTH = 10

export function formatTokens(n: number): string {
  if (n >= 1_000_000) return `${+(n / 1_000_000).toFixed(1)}M`
  if (n >= 1_000) return `${+(n / 1_000).toFixed(1)}k`
  return `${n}`
}

export function bar(percent: number): string {
  const filled = Math.min(BAR_WIDTH, Math.max(0, Math.round((percent * BAR_WIDTH) / 100)))
  return '█'.repeat(filled) + '░'.repeat(BAR_WIDTH - filled)
}

export function level(percent: number): 'success' | 'warning' | 'error' {
  if (percent >= 80) return 'error'
  if (percent >= 50) return 'warning'
  return 'success'
}
