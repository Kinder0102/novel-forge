import { computed, type Ref } from 'vue'
import { useI18n } from 'vue-i18n'

export interface StatItem {
  key: string
  label: string
  subtitle: string
  count: number
  icon: string
  path: string
}

export function useNovelStats(
  baseUrl: Ref<string>,
  worldbuildingCount: Ref<number>,
  characterCount: Ref<number>,
  outlineCount: Ref<number>,
  sceneCount: Ref<number>,
  chapterCount: Ref<number>,
) {
  const { t } = useI18n()

  const stats = computed<StatItem[]>(() => [
    {
      key: 'worldbuilding',
      label: t('dashboard.stats.worldbuilding'),
      subtitle: t('dashboard.stats.worldbuildingSub'),
      count: worldbuildingCount.value ?? 0,
      icon: 'fa-solid fa-globe',
      path: `${baseUrl.value}/worldbuilding`,
    },
    {
      key: 'character',
      label: t('dashboard.stats.character'),
      subtitle: t('dashboard.stats.characterSub'),
      count: characterCount.value ?? 0,
      icon: 'fa-solid fa-users',
      path: `${baseUrl.value}/character`,
    },
    {
      key: 'outline',
      label: t('dashboard.stats.outline'),
      subtitle: t('dashboard.stats.outlineSub'),
      count: outlineCount.value ?? 0,
      icon: 'fa-solid fa-list-ol',
      path: `${baseUrl.value}/outline`,
    },
    {
      key: 'scene',
      label: t('dashboard.stats.scene'),
      subtitle: t('dashboard.stats.sceneSub'),
      count: sceneCount.value ?? 0,
      icon: 'fa-solid fa-clapperboard',
      path: `${baseUrl.value}/scene/:outlineId`,
    },
    {
      key: 'chapter',
      label: t('dashboard.stats.chapter'),
      subtitle: t('dashboard.stats.chapterSub'),
      count: chapterCount.value ?? 0,
      icon: 'fa-solid fa-book-open',
      path: `${baseUrl.value}/chapter/:outlineId`,
    },
  ])

  return { stats }
}
