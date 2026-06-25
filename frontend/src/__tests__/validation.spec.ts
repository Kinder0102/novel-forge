import { describe, it, expect } from 'vitest'
import {
  createUrlOrEmpty,
  createRequiredString,
  createRequiredNumber,
  optionalText,
  createSettingsModuleSchema,
  createNovelCreateSchema,
  createNovelUpdateSchema,
  createCharacterSchema,
  createWorldbuildingSchema,
  createOutlineSchema,
  createSceneSchema,
} from '../utils/validation'

describe('validation — 共用規則', () => {
  describe('createUrlOrEmpty', () => {
    const urlOrEmpty = createUrlOrEmpty()

    it('空字串可通過', () => {
      expect(urlOrEmpty.safeParse('').success).toBe(true)
    })

    it('有效的 http URL 可通過', () => {
      expect(urlOrEmpty.safeParse('http://localhost:8000').success).toBe(true)
    })

    it('有效的 https URL 可通過', () => {
      expect(urlOrEmpty.safeParse('https://api.example.com/v1').success).toBe(true)
    })

    it('非 URL 字串應失敗', () => {
      expect(urlOrEmpty.safeParse('not-a-url').success).toBe(false)
    })
  })

  describe('createRequiredString', () => {
    const requiredString = createRequiredString()

    it('非空字串可通過', () => {
      expect(requiredString.safeParse('hello').success).toBe(true)
    })

    it('純空白字串應失敗', () => {
      expect(requiredString.safeParse('   ').success).toBe(false)
    })

    it('空字串應失敗', () => {
      expect(requiredString.safeParse('').success).toBe(false)
    })
  })

  describe('createRequiredNumber', () => {
    const requiredNumber = createRequiredNumber()

    it('正整數可通過', () => {
      expect(requiredNumber.safeParse(5).success).toBe(true)
    })

    it('0 應失敗', () => {
      expect(requiredNumber.safeParse(0).success).toBe(false)
    })

    it('負數應失敗', () => {
      expect(requiredNumber.safeParse(-1).success).toBe(false)
    })
  })

  describe('optionalText', () => {
    it('空字串可通過', () => {
      expect(optionalText.safeParse('').success).toBe(true)
    })

    it('undefined 可通過', () => {
      expect(optionalText.safeParse(undefined).success).toBe(true)
    })
  })
})

describe('validation — schema', () => {
  describe('createSettingsModuleSchema', () => {
    const settingsModuleSchema = createSettingsModuleSchema()

    it('全空欄位可通過', () => {
      const result = settingsModuleSchema.safeParse({
        api_key: '',
        base_url: '',
        model: '',
        system_prompt: '',
        user_prompt_template: '',
      })
      expect(result.success).toBe(true)
    })

    it('無效 base_url 應失敗', () => {
      const result = settingsModuleSchema.safeParse({
        api_key: '',
        base_url: 'invalid',
        model: '',
        system_prompt: '',
        user_prompt_template: '',
      })
      expect(result.success).toBe(false)
    })
  })

  describe('createNovelCreateSchema', () => {
    const novelCreateSchema = createNovelCreateSchema()

    it('空白標題應失敗', () => {
      expect(novelCreateSchema.safeParse({ title: '', description: '' }).success).toBe(false)
    })

    it('有效標題可通過', () => {
      expect(novelCreateSchema.safeParse({ title: '我的小說', description: '' }).success).toBe(true)
    })
  })

  describe('createCharacterSchema', () => {
    const characterSchema = createCharacterSchema()

    it('空白名稱應失敗', () => {
      expect(characterSchema.safeParse({ name: '' }).success).toBe(false)
    })

    it('有效名稱可通過', () => {
      expect(characterSchema.safeParse({ name: '主角', role: '英雄' }).success).toBe(true)
    })
  })

  describe('createWorldbuildingSchema', () => {
    const worldbuildingSchema = createWorldbuildingSchema()

    it('空白標題應失敗', () => {
      expect(worldbuildingSchema.safeParse({ title: '' }).success).toBe(false)
    })

    it('有效標題可通過', () => {
      expect(worldbuildingSchema.safeParse({ title: '奇幻世界' }).success).toBe(true)
    })
  })

  describe('createOutlineSchema', () => {
    const outlineSchema = createOutlineSchema()

    it('空白標題應失敗', () => {
      expect(outlineSchema.safeParse({ title: '' }).success).toBe(false)
    })

    it('有效標題可通過', () => {
      expect(outlineSchema.safeParse({ title: '第一章' }).success).toBe(true)
    })
  })

  describe('createSceneSchema', () => {
    const sceneSchema = createSceneSchema()

    it('scene_number 為 0 應失敗', () => {
      expect(sceneSchema.safeParse({ scene_number: 0, title: '場景' }).success).toBe(false)
    })

    it('有效資料可通過', () => {
      expect(sceneSchema.safeParse({ scene_number: 1, title: '場景一' }).success).toBe(true)
    })
  })
})
