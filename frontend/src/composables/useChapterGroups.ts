import { computed, type Ref } from 'vue'
import { useI18n } from 'vue-i18n'


interface ChapterGroupItem {
  id?: number
  ctId: number
  idx: number
  title: string
  content?: string
  summary?: string
  chapter_title_id: number
}

interface ChapterGroup {
  outlineId: number
  outlineTitle: string
  chapters: ChapterGroupItem[]
}

export function useChapterGroups(
  allOutlines: Ref<{ id: number; title?: string; chapter_titles?: { id: number; idx: number; title: string; outline_id: number }[] }[]>,
  allChapters: Ref<{ id?: number; chapter_title_id: number; content?: string; summary?: string }[]>,
  allChapterTitles: Ref<{ id: number; outline_id: number; idx: number; title: string }[]>,
) {
  const { t } = useI18n()
  const validTitle = (vt: unknown): string | null => (vt && vt !== 'undefined' && String(vt).trim()) || null
  const chapterGroups = computed<ChapterGroup[]>(() => {
    const titles = allChapterTitles?.value ?? []
    const chapters = allChapters?.value ?? []
    const outlines = allOutlines?.value ?? []

    const titleMap = new Map<number, { id: number; outline_id: number; idx: number; title: string }>()
    for (const ct of titles) {
      titleMap.set(ct.id, ct)
    }
    const chaptersWithContent = chapters.filter(
      (c) => c?.content && String(c.content).trim().length > 0,
    )
    const map = new Map<number, ChapterGroup>()
    for (const ch of chaptersWithContent) {
      const ct = titleMap.get(ch.chapter_title_id)
      if (!ct) continue
      const outlineId = ct.outline_id
      if (!map.has(outlineId)) {
        const outline = outlines.find((o) => o.id === outlineId)
        map.set(outlineId, {
          outlineId,
          outlineTitle: validTitle(outline?.title) || t('chapter.outlineFallback', { id: outlineId }),
          chapters: [],
        })
      }
      map.get(outlineId)!.chapters.push({
        ...ch,
        title: validTitle(ct.title) || t('chapter.untitled'),
        idx: ct.idx,
        ctId: ct.id,
        chapter_title_id: ch.chapter_title_id,
      })
    }
    const groups = Array.from(map.values())
    groups.sort((a, b) => {
      const oa = outlines.find((o) => o.id === a.outlineId)
      const ob = outlines.find((o) => o.id === b.outlineId)
      return (oa?.id || 0) - (ob?.id || 0)
    })
    for (const g of groups) {
      const seen = new Set<number>()
      g.chapters = g.chapters.filter((ch) => {
        const key = ch.ctId
        if (seen.has(key)) return false
        seen.add(key)
        return true
      })
      g.chapters.sort((a, b) => a.idx - b.idx)
    }
    return groups
  })

  return { chapterGroups }
}
