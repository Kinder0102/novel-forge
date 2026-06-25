import { defineStore } from 'pinia'
import { extractErrorMessage } from '../utils/error'

type BaseRecord = { id?: number | string; [key: string]: unknown }

export interface CrudStoreConfig<
  T extends BaseRecord = BaseRecord,
  TExtraState extends Record<string, unknown> = Record<string, unknown>,
  TActions extends Record<string, unknown> = Record<string, unknown>
> {
  storeId: string
  itemsKey: string
  apiModule: Record<string, (...args: unknown[]) => unknown>
  extraState?: TExtraState | (() => TExtraState)
  extraActions?: TActions & ThisType<CrudStoreState<T, TExtraState> & CrudStoreActions<T, TExtraState, TActions>>
}

export interface CrudStoreState<T extends BaseRecord, TExtraState extends Record<string, unknown>> {
  [key: string]: T[] | T | null | boolean | string | null | unknown
  current: T | null
  loading: boolean
  error: string | null
  _pendingRequests: number
}

export interface CrudStoreActions<
  T extends BaseRecord,
  TExtraState extends Record<string, unknown> = Record<string, unknown>,
  TActions extends Record<string, unknown> = Record<string, unknown>
> {
  fetchAll(...args: unknown[]): Promise<void>
  fetchOne(id: number | string): Promise<void>
  create(data: Partial<T>): Promise<T>
  update(id: number | string, data: Partial<T>): Promise<T>
  remove(id: number | string): Promise<void>
}

function cap(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1)
}

export function createCrudStore<
  T extends BaseRecord = BaseRecord,
  TExtraState extends BaseRecord = BaseRecord,
  TActions extends BaseRecord = BaseRecord
>(config: CrudStoreConfig<T, TExtraState, TActions>) {
  const { storeId, itemsKey, apiModule, extraState = {} as TExtraState, extraActions = {} as TActions } = config
  const name = cap(storeId)

  return defineStore(storeId, {
    state: () => ({
      [itemsKey]: [] as T[],
      current: null as T | null,
      loading: false,
      error: null as string | null,
      _pendingRequests: 0,
      ...(typeof extraState === 'function' ? (extraState as () => TExtraState)() : extraState),
    }),

    actions: {
      async fetchAll(...args: unknown[]) {
        this._pendingRequests++
        this.loading = true
        this.error = null
        try {
          const api = apiModule as Record<string, (...a: unknown[]) => Promise<{ data: T[] }>>
          const fn = api[`get${name}s`] || api[`get${name}`]
          if (!fn) throw new Error('error.apiNotFound')
          const res = await fn(...args)
          this[itemsKey] = res.data
        } catch (e: unknown) {
          this.error = extractErrorMessage(e)
        } finally {
          this._pendingRequests--
          this.loading = this._pendingRequests > 0
        }
      },

      async fetchOne(id: number | string) {
        this._pendingRequests++
        this.loading = true
        this.error = null
        try {
          const api = apiModule as Record<string, (id: number | string) => Promise<{ data: T }>>
          const fn = api[`get${name}`]
          if (!fn) throw new Error('error.apiNotFound')
          const res = await fn(id)
          this.current = res.data
        } catch (e: unknown) {
          this.error = extractErrorMessage(e)
        } finally {
          this._pendingRequests--
          this.loading = this._pendingRequests > 0
        }
      },

      async create(data: Partial<T>) {
        this._pendingRequests++
        this.loading = true
        this.error = null
        try {
          const api = apiModule as Record<string, (d: Partial<T>) => Promise<{ data: T }>>
          const fn = api[`create${name}`]
          if (!fn) throw new Error('error.apiNotFound')
          const res = await fn(data)
          this[itemsKey].push(res.data)
          return res.data
        } catch (e: unknown) {
          this.error = extractErrorMessage(e)
        } finally {
          this._pendingRequests--
          this.loading = this._pendingRequests > 0
        }
      },

      async update(id: number | string, data: Partial<T>) {
        this._pendingRequests++
        this.loading = true
        this.error = null
        try {
          const api = apiModule as Record<string, (id: number | string, d: Partial<T>) => Promise<{ data: T }>>
          const fn = api[`update${name}`]
          if (!fn) throw new Error('error.apiNotFound')
          const res = await fn(id, data)
          const result = res.data
          const item = this[itemsKey].find((o: T) => o.id === id)
          if (item) Object.assign(item, result)
          if (this.current?.id === id) this.current = result as T
          return result
        } catch (e: unknown) {
          this.error = extractErrorMessage(e)
        } finally {
          this._pendingRequests--
          this.loading = this._pendingRequests > 0
        }
      },

      async remove(id: number | string) {
        this._pendingRequests++
        this.loading = true
        this.error = null
        try {
          const api = apiModule as Record<string, (id: number | string) => Promise<unknown>>
          const fn = api[`delete${name}`]
          if (!fn) throw new Error('error.apiNotFound')
          await fn(id)
          this[itemsKey] = this[itemsKey].filter((o: T) => o.id !== id)
          if (this.current?.id === id) this.current = null
        } catch (e: unknown) {
          this.error = extractErrorMessage(e)
        } finally {
          this._pendingRequests--
          this.loading = this._pendingRequests > 0
        }
      },

      ...extraActions,
    },
  })
}
