import { expect, test } from 'claude-code/testing'

import { bar, formatTokens, level } from './format'

test('formats token counts', () => {
  expect(formatTokens(950)).toBe('950')
  expect(formatTokens(45_200)).toBe('45.2k')
  expect(formatTokens(200_000)).toBe('200k')
  expect(formatTokens(1_000_000)).toBe('1M')
})

test('fills the bar by percent', () => {
  expect(bar(0)).toBe('░░░░░░░░░░')
  expect(bar(23)).toBe('██░░░░░░░░')
  expect(bar(100)).toBe('██████████')
})

test('colors by threshold', () => {
  expect(level(49)).toBe('success')
  expect(level(50)).toBe('warning')
  expect(level(80)).toBe('error')
})
