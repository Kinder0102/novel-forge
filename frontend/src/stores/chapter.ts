import { createCrudStore } from './crudStoreFactory'
import { extractErrorMessage } from '../utils/error'
import * as api from '../api'
import type { ChapterContentData } from '../types'

export type ChapterContent = ChapterContentData & {
  word_count?: number
  status?: string
}

export interface GenerateChapterRequest {
  novel_id?: number
  chapter_title_id: number
  chapter_title?: string
  previous_summary?: string
  context?: string
  description?: string
}

export const useChapterStore = createCrudStore<ChapterContent>({
  storeId: 'chapter',
  itemsKey: 'chapters',
  apiModule: api,
  extraActions: {
    async fetchAll(outlineId: number) {
      this.loading = true
      this.error = null
      try {
        const res = await api.getChapters(outlineId)
        this.chapters = (res.data || []).filter(
          (c, i, arr) => arr.findIndex((x) => x.chapter_title_id === c.chapter_title_id) === i,
        )
      } catch (e: unknown) {
        this.error = extractErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    async generateChapter(data: GenerateChapterRequest) {
      this.loading = true
      this.error = null
      try {
        const res = await api.generateChapter(data)
        const idx = this.chapters.findIndex((c) => c.chapter_title_id === data.chapter_title_id)
        if (idx !== -1) {
          this.chapters[idx] = res.data
        } else {
          this.chapters.push(res.data)
        }
        return res.data
      } catch (e: unknown) {
        this.error = extractErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    async regenerateSummary(chapterId: number) {
      const res = await api.regenerateSummary(chapterId)
      const idx = this.chapters.findIndex((c) => c.id === chapterId)
      if (idx !== -1) this.chapters[idx] = res.data
      return res.data
    },
    async loadAllForOutlines(outlineIds: number[]) {
      this.loading = true
      this.error = null
      try {
        const results = await Promise.allSettled(outlineIds.map((id) => api.getChapters(id)))
        this.chapters = results
          .filter((r): r is PromiseFulfilledResult<{ data: ChapterContent[] }> => r.status === 'fulfilled')
          .flatMap((r) => r.value.data || [])
          .filter((c, i, arr) => arr.findIndex((x) => x.chapter_title_id === c.chapter_title_id) === i)
      } catch (e: unknown) {
        this.error = extractErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
  },
})
