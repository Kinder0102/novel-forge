import { describe, it, expect, beforeEach, vi } from 'vitest'
import axios from 'axios'
import { setActivePinia, createPinia } from 'pinia'
import type { AxiosError } from 'axios'
import { createCrudStore, type CrudStoreConfig } from '../stores/crudStoreFactory'


function makeAxiosError(message: string, detail?: string): AxiosError {
  const err = new axios.AxiosError(
    message,
    'ERR_BAD_REQUEST',
    undefined,
    undefined,
    {
      status: 400,
      data: detail ? { detail } : undefined,
      statusText: 'Bad Request',
      headers: {} as any,
      config: {} as any,
    },
  )
  return err
}


type TestItem = { id?: number; name: string; [key: string]: unknown }


function makeFakeApi(): Record<string, (...args: unknown[]) => unknown> {
  return {
    getTests: vi.fn(),
    getTest: vi.fn(),
    createTest: vi.fn(),
    updateTest: vi.fn(),
    deleteTest: vi.fn(),
  }
}

describe('crudStoreFactory', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  function makeConfig(apiModule: Record<string, (...args: unknown[]) => unknown>): CrudStoreConfig<TestItem> {
    return {
      storeId: 'test',
      itemsKey: 'tests',
      apiModule,
    }
  }

  describe('fetchAll', () => {
    it('成功時應設置 tests 陣列', async () => {
      const api = makeFakeApi()
      const items = [{ id: 1, name: 'A' }, { id: 2, name: 'B' }]
      ;(api.getTests as any).mockResolvedValue({ data: items })

      const useStore = createCrudStore<TestItem>(makeConfig(api))
      const store = useStore()
      await store.fetchAll()

      expect(store.tests).toEqual(items)
      expect(store.loading).toBe(false)
      expect(store.error).toBeNull()
    })

    it('AxiosError 時應設置 error', async () => {
      const api = makeFakeApi()
      const axiosErr = makeAxiosError('Network Error', '連線失敗')
      ;(api.getTests as any).mockRejectedValue(axiosErr)

      const useStore = createCrudStore<TestItem>(makeConfig(api))
      const store = useStore()
      await store.fetchAll()

      expect(store.loading).toBe(false)
      expect(store.error).toBe('連線失敗')
    })

    it('一般 Error 時應設置 error.message', async () => {
      const api = makeFakeApi()
      ;(api.getTests as any).mockRejectedValue(new Error('自訂錯誤'))

      const useStore = createCrudStore<TestItem>(makeConfig(api))
      const store = useStore()
      await store.fetchAll()

      expect(store.error).toBe('自訂錯誤')
    })
  })

  describe('create', () => {
    it('成功時應將項目加入陣列', async () => {
      const api = makeFakeApi()
      ;(api.createTest as any).mockResolvedValue({ data: { id: 3, name: 'C' } })

      const useStore = createCrudStore<TestItem>(makeConfig(api))
      const store = useStore()
      const result = await store.create({ name: 'C' })

      expect(result).toEqual({ id: 3, name: 'C' })
      expect(store.tests).toHaveLength(1)
      expect(store.tests[0]).toEqual({ id: 3, name: 'C' })
    })
  })

  describe('update', () => {
    it('成功時應更新陣列中的項目', async () => {
      const api = makeFakeApi()
      ;(api.updateTest as any).mockResolvedValue({ data: { id: 1, name: '已更新' } })

      const useStore = createCrudStore<TestItem>(makeConfig(api))
      const store = useStore()
      store.tests = [{ id: 1, name: '原始' }]
      await store.update(1, { name: '已更新' })

      expect(store.tests[0].name).toBe('已更新')
    })
  })

  describe('remove', () => {
    it('成功時應從陣列移除項目', async () => {
      const api = makeFakeApi()
      ;(api.deleteTest as any).mockResolvedValue(undefined)

      const useStore = createCrudStore<TestItem>(makeConfig(api))
      const store = useStore()
      store.tests = [{ id: 1, name: 'A' }, { id: 2, name: 'B' }]
      await store.remove(1)

      expect(store.tests).toHaveLength(1)
      expect(store.tests[0].id).toBe(2)
    })
  })

  describe('extraActions', () => {
    it('自訂 action 可存取 this', async () => {
      const api = makeFakeApi()

      const useStore = createCrudStore<TestItem>({
        storeId: 'test',
        itemsKey: 'tests',
        apiModule: api,
        extraActions: {
          async customAction(name: string) {
            this.tests.push({ id: 99, name: name } as TestItem)
            return name
          },
        } as any,
      })

      const store = useStore() as any
      const result = await store.customAction('自訂')
      expect(result).toBe('自訂')
      expect(store.tests).toHaveLength(1)
      expect(store.tests[0].name).toBe('自訂')
    })
  })
})
