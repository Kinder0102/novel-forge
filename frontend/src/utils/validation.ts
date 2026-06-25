import { z } from 'zod'
import i18n from '../i18n'




export function createUrlOrEmpty() {
  const t = i18n.global.t
  return z.string().refine((v) => !v || /^https?:\/\/.+/.test(v), t('validation.urlFormat'))
}


export function createRequiredString() {
  const t = i18n.global.t
  return z.string().trim().min(1, t('validation.required'))
}


export function createRequiredNumber() {
  const t = i18n.global.t
  return z.number({ invalid_type_error: t('validation.pleaseEnterNumber') }).min(1, t('validation.pleaseEnterValidNumber'))
}


export const optionalText = z.string().optional()


export function createSettingsModuleSchema() {
  return z.object({
    api_key: optionalText,
    base_url: createUrlOrEmpty(),
    model: optionalText,
    system_prompt: optionalText,
    user_prompt_template: optionalText,
  })
}

export function createNovelCreateSchema() {
  return z.object({
    title: createRequiredString(),
    description: optionalText,
  })
}

export function createNovelUpdateSchema() {
  return z.object({
    writing_style: optionalText,
  })
}

export function createCharacterSchema() {
  return z.object({
    name: createRequiredString(),
    role: optionalText,
    personality: optionalText,
    background: optionalText,
    appearance: optionalText,
    summary: optionalText,
  })
}

export function createWorldbuildingSchema() {
  return z.object({
    title: createRequiredString(),
    genre: optionalText,
    description: optionalText,
    setting: optionalText,
    rules: optionalText,
    summary: optionalText,
  })
}

export function createOutlineSchema() {
  return z.object({
    title: createRequiredString(),
    description: optionalText,
    summary: optionalText,
  })
}

export function createSceneSchema() {
  const t = i18n.global.t
  return z.object({
    scene_number: z.number({ invalid_type_error: t('validation.pleaseEnterNumber') }).positive(t('validation.positiveNumber')),
    title: createRequiredString(),
    description: optionalText,
    summary: optionalText,
  })
}
