import i18n from '../i18n'

const t = i18n.global.t







export function formatTime(dateStr: string | undefined | null): string {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  if (isNaN(d.getTime())) return ''
  const diffDay = Math.floor((Date.now() - d.getTime()) / 86400000)
  if (diffDay < 1) return t('format.today')
  if (diffDay < 7) return t('format.daysAgo', { n: diffDay })
  return `${d.getFullYear()}/${(d.getMonth() + 1).toString().padStart(2, '0')}/${d.getDate().toString().padStart(2, '0')}`
}
