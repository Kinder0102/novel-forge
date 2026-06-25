import axios from 'axios'
import i18n from '../i18n'

const ERROR_CODE_MAP: Record<string, string> = {
  HTTP_404: 'error.resourceNotFound',
  VALIDATION_ERROR: 'error.validationError',
  INTERNAL_ERROR: 'error.internalError',
}

const DETAIL_KEYWORD_MAP: [RegExp, string][] = [
  [/大綱不存在/, 'error.outlineNotFound'],
  [/章節標題不存在/, 'error.chapterNotFound'],
  [/章節不存在/, 'error.chapterNotFound'],
  [/worldbuilding_id.*必填/, 'error.missingWorldbuildingId'],
  [/無效的模組名稱/, 'error.invalidModuleName'],
  [/不可刪除\s*default/, 'error.cannotDeleteDefault'],
  [/不存在/, 'error.resourceNotFound'],
]


export function extractErrorMessage(e: unknown): string {
  if (axios.isAxiosError(e)) {
    const detail = e.response?.data?.detail as string | undefined
    const errorCode = e.response?.data?.error_code as string | undefined

    
    if (errorCode && ERROR_CODE_MAP[errorCode]) {
      return i18n.global.t(ERROR_CODE_MAP[errorCode])
    }

    
    if (detail) {
      for (const [pattern, i18nKey] of DETAIL_KEYWORD_MAP) {
        if (pattern.test(detail)) {
          return i18n.global.t(i18nKey)
        }
      }
    }

    
    return detail || e.message
  }
  if (e instanceof Error) {
    if (typeof e.message === 'string' && e.message.startsWith('error.')) {
      return i18n.global.t(e.message)
    }
    return e.message
  }
  return i18n.global.t('error.unknown')
}
