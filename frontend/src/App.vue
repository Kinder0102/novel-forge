<template>
  <div>
    <BaseNavBar :nav-items="navItems" :novel-title="novelTitle" :active-mode="activeMode" />

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <router-view />
    </main>

    <TaskPanel />
  </div>
</template><script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useNovelStore } from './stores/novel'
import BaseNavBar from './components/BaseNavBar.vue'
import TaskPanel from './components/TaskPanel.vue'

const route = useRoute()
const novelStore = useNovelStore()
const { t } = useI18n()

const isNovelRoute = computed(() => !!route.matched.find(r => r.name?.startsWith('Novel')))

const novelId = computed(() => route.params.novelId || null)

const navItems = computed(() => {
  if (isNovelRoute.value && novelId.value) {
    return [
      { path: `/novel/${novelId.value}`, label: t('nav.dashboard'), icon: 'fa-solid fa-chart-pie' },
      { path: `/novel/${novelId.value}/worldbuilding`, label: t('nav.worldbuilding'), icon: 'fa-solid fa-globe' },
      { path: `/novel/${novelId.value}/character`, label: t('nav.character'), icon: 'fa-solid fa-users' },
      { path: `/novel/${novelId.value}/outline`, label: t('nav.outline'), icon: 'fa-solid fa-list' }
    ]
  }
  return [
    { path: '/', label: t('nav.home'), icon: 'fa-solid fa-home' },
    { path: '/projects', label: t('nav.projects'), icon: 'fa-solid fa-folder-open' },
    { path: '/settings', label: t('nav.settings'), icon: 'fa-solid fa-gear' }
  ]
})

const novelTitle = computed(() => {
  if (isNovelRoute.value && novelStore.current) {
    return novelStore.current.title || t('common.loading')
  }
  return ''
})

const activeMode = computed(() => isNovelRoute.value ? 'prefix' : 'exact')
</script>