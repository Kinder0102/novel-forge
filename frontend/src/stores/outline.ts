import { createCrudStore } from './crudStoreFactory'
import { extractErrorMessage } from '../utils/error'
import * as api from '../api'
import type { OutlineData } from '../types'

export const useOutlineStore = createCrudStore<OutlineData>({
  storeId: 'outline',
  itemsKey: 'outlines',
  apiModule: api,
  extraActions: {
    async generateOutline(data: Record<string, unknown>) {
      this.loading = true
      this.error = null
      try {
        const res = await api.generateOutline(data)
        const outline = res.data
        if (outline) {
          this.outlines.push(outline)
        }
        return outline
      } catch (e: unknown) {
        this.error = extractErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    async regenerateSummary(outlineId: number) {
      const res = await api.regenerateOutlineSummary(outlineId)
      const idx = this.outlines.findIndex((o) => o.id === outlineId)
      if (idx !== -1) this.outlines[idx] = res.data
      if (this.current?.id === outlineId) this.current = res.data
      return res.data
    },
  },
})
