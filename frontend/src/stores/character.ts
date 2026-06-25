import axios from 'axios'
import { extractErrorMessage } from '../utils/error'
import { createCrudStore } from './crudStoreFactory'
import * as api from '../api'

export interface Character {
  id: number
  novel_id: number
  name: string
  role?: string
  personality?: string
  background?: string
  appearance?: string
  created_at?: string
  updated_at?: string
}

export const useCharacterStore = createCrudStore<Character>({
  storeId: 'character',
  itemsKey: 'characters',
  apiModule: api,
  extraActions: {
    async generateCharacters(data: Record<string, unknown>) {
      this.loading = true
      this.error = null
      try {
        const res = await api.generateCharacters(data)
        const characters = res.data
        if (Array.isArray(characters)) {
          this.characters.push(...characters)
        } else if (characters) {
          this.characters.push(characters)
        }
        return characters
      } catch (e: unknown) {
        this.error = extractErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    async regenerateSummary(charId: number) {
      const res = await api.regenerateCharacterSummary(charId)
      const idx = this.characters.findIndex((c) => c.id === charId)
      if (idx !== -1) this.characters[idx] = res.data
      return res.data
    },
  },
})
