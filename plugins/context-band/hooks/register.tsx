import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import { bar, formatTokens, level } from './format'

// Bumped on each measurement so the band redraws with fresh figures.
const tick = atom({ plugin: 'context-band', key: 'tick' } as const, 0)

export const register: Register = on => {
  on('session.measure', async ($, e, next) => {
    await update($, tick, n => n + 1)

    return next(e)
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    await read($, tick)
    if (e.props.hasSurvey) {
      return next(e)
    }

    const { context } = await $.session.usage()
    const model = await $.session.model()
    const tokens = context.tokens ?? 0
    const percent = context.percent ?? 0
    const { Box, Text } = $.ui.resolve(e)

    return (
      <Box justifyContent="flex-end" paddingY={1}>
        <Text dimColor>
          {model} | {formatTokens(tokens)} / {formatTokens(context.window)} |{' '}
        </Text>
        <Text color={level(percent)}>
          {bar(percent)} {percent}%
        </Text>
      </Box>
    )
  })
}
