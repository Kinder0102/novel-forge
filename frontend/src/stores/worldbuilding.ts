import { createCrudStore } from './crudStoreFactory'
import * as api from '../api'
import type { WorldbuildingData } from '../types'

export type { WorldbuildingData as Worldbuilding }

export const useWorldbuildingStore = createCrudStore<WorldbuildingData>({
  storeId: 'worldbuilding',
  itemsKey: 'worldbuildings',
  apiModule: api,
  extraActions: {
    async regenerateSummary(wbId: number) {
      const res = await api.regenerateWorldbuildingSummary(wbId)
      const idx = this.worldbuildings.findIndex((w) => w.id === wbId)
      if (idx !== -1) this.worldbuildings[idx] = res.data
      return res.data
    },
  },
})
