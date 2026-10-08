import { expect, test } from 'claude-code/testing'

const BAND = {
  component: 'AbovePrompt',
  props: { hasSurvey: false, isWorking: false, maxRows: 10 },
} as const

test('draws model, tokens and bar', async ($, on) => {
  on('session.usage', () => ({
    value: {
      startedAt: 0,
      context: { tokens: 45_200, window: 200_000, percent: 23 },
      rateLimits: [],
    },
  }))
  on('session.model', () => ({ value: 'claude-opus-5-5' }))
  on('ui.render', () => ({ type: 'Box', props: {}, children: [] }))

  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({ plugin: 'context-band', surface, ...BAND })
    expect(await ui.find({ type: 'Text', text: /claude-opus-5-5 \| 45\.2k \/ 200k/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /██░░░░░░░░ 23%/ })).toBeDefined()
    await ui.unmount()
  }
})
