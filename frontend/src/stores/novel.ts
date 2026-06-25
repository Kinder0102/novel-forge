import { createCrudStore } from './crudStoreFactory'
import * as api from '../api'
import type { NovelData } from '../types'

export type { NovelData as Novel }

export const useNovelStore = createCrudStore<NovelData>({
  storeId: 'novel',
  itemsKey: 'novels',
  apiModule: api,
  extraActions: {
    setCurrent(novel: NovelData) {
      this.current = novel
    },
  },
})
