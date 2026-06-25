<template>
  <div class="space-y-8">
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-16">
      <font-awesome-icon icon="fa-solid fa-spinner" spin class="text-4xl text-indigo-500 mb-4" />
      <p class="text-gray-500 text-lg">載入儀表板資料中...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-16">
      <font-awesome-icon icon="fa-solid fa-exclamation-triangle" class="text-4xl text-amber-500 mb-4" />
      <p class="text-gray-700 text-lg font-semibold mb-2">無法載入儀表板資料</p>
      <p class="text-gray-500 mb-4">{{ error }}</p>
      <button
        @click="loadDashboard"
        class="inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium"
      >
        <font-awesome-icon icon="fa-solid fa-undo" class="mr-2" />
        重新載入
      </button>
    </div>

    <!-- Dashboard Content -->
    <template v-else>
      <!-- Stats Overview -->
      <section>
        <h2 class="text-lg font-semibold text-gray-900 mb-4">創作概覽</h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
          <router-link
            v-for="stat in stats"
            :key="stat.key"
            :to="stat.path"
            class="bg-white rounded-xl shadow-sm p-5 hover:shadow-md hover:-translate-y-0.5 transition-all duration-200 group"
          >
            <div class="flex items-center justify-between mb-3">
              <div
                class="w-10 h-10 rounded-lg flex items-center justify-center"
                :class="stat.bgClass"
              >
                <font-awesome-icon :icon="stat.icon" :class="stat.iconClass" />
              </div>
              <span class="text-3xl font-extrabold" :class="stat.countClass">{{ stat.count }}</span>
            </div>
            <p class="text-sm font-medium text-gray-600 group-hover:text-gray-900 transition-colors">{{ stat.label }}</p>
          </router-link>
        </div>
      </section>

      <!-- Quick Entry Cards -->
      <section>
        <h2 class="text-lg font-semibold text-gray-900 mb-4">快速入口</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <router-link
            v-for="mod in modules"
            :key="mod.path"
            :to="mod.path"
            class="bg-white rounded-xl shadow-sm p-6 hover:shadow-lg hover:-translate-y-1 transition-all duration-200 group flex flex-col"
          >
            <div class="flex items-center space-x-3 mb-3">
              <div class="w-11 h-11 rounded-xl flex items-center justify-center transition-colors" :class="mod.bgClass">
                <font-awesome-icon :icon="mod.icon" :class="mod.iconClass" />
              </div>
              <div>
                <h3 class="text-base font-semibold text-gray-900">{{ mod.title }}</h3>
                <span class="text-xs text-gray-400">{{ mod.count }} 項</span>
              </div>
            </div>
            <p class="text-sm text-gray-500 flex-1 mb-4">{{ mod.desc }}</p>
            <span class="inline-flex items-center text-sm font-medium text-indigo-600 group-hover:text-indigo-800 transition-colors">
              前往
              <font-awesome-icon icon="fa-solid fa-arrow-right" class="ml-1.5 text-xs" />
            </span>
          </router-link>
        </div>
      </section>

      <!-- Recent Activity -->
      <section v-if="recentItems.length > 0">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">最近活動</h2>
        <div class="bg-white rounded-xl shadow-sm overflow-hidden">
          <div class="divide-y divide-gray-100">
            <div
              v-for="item in recentItems"
              :key="`${item.type}-${item.id}`"
              class="flex items-center px-5 py-4 hover:bg-gray-50 transition-colors"
            >
              <div class="w-9 h-9 rounded-lg flex items-center justify-center mr-4 flex-shrink-0" :class="item.bgClass">
                <font-awesome-icon :icon="item.icon" :class="item.iconClass" class="text-sm" />
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 truncate">{{ item.name }}</p>
                <p class="text-xs text-gray-400 mt-0.5">
                  {{ item.typeLabel }}
                  <span v-if="item.time" class="ml-2">{{ formatTime(item.time) }}</span>
                </p>
              </div>
              <router-link
                :to="item.path"
                class="ml-4 text-xs font-medium text-indigo-600 hover:text-indigo-800 transition-colors flex-shrink-0"
              >
                檢視
              </router-link>
            </div>
          </div>
        </div>
      </section>

      <!-- Empty State -->
      <div v-if="isAllEmpty" class="text-center py-12 bg-white rounded-xl shadow-sm">
        <font-awesome-icon icon="fa-solid fa-feather" class="text-5xl text-gray-300 mb-4" />
        <p class="text-gray-500 text-lg mb-2">尚無任何創作資料</p>
        <p class="text-gray-400 text-sm mb-6">從世界觀開始，逐步構建你的故事世界</p>
        <router-link
          to="/worldbuilding"
          class="inline-flex items-center px-5 py-2.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium"
        >
          <font-awesome-icon icon="fa-solid fa-plus" class="mr-2" />
          建立世界觀
        </router-link>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import * as api from '../api'

const loading = ref(true)
const error = ref(null)

// Accumulated data
const allWorldbuildings = ref([])
const allCharacters = ref([])
const allOutlines = ref([])
const allScenes = ref([])
const allChapters = ref([])

// Stats definition
const stats = computed(() => [
  {
    key: 'worldbuilding',
    label: '世界觀',
    count: allWorldbuildings.value.length,
    icon: 'fa-solid fa-globe',
    bgClass: 'bg-indigo-100 group-hover:bg-indigo-200',
    iconClass: 'text-indigo-600',
    countClass: 'text-indigo-600',
    path: '/worldbuilding'
  },
  {
    key: 'character',
    label: '角色',
    count: allCharacters.value.length,
    icon: 'fa-solid fa-users',
    bgClass: 'bg-emerald-100 group-hover:bg-emerald-200',
    iconClass: 'text-emerald-600',
    countClass: 'text-emerald-600',
    path: '/character'
  },
  {
    key: 'outline',
    label: '大綱',
    count: allOutlines.value.length,
    icon: 'fa-solid fa-list',
    bgClass: 'bg-amber-100 group-hover:bg-amber-200',
    iconClass: 'text-amber-600',
    countClass: 'text-amber-600',
    path: '/outline'
  },
  {
    key: 'scene',
    label: '場景',
    count: allScenes.value.length,
    icon: 'fa-solid fa-clapperboard',
    bgClass: 'bg-rose-100 group-hover:bg-rose-200',
    iconClass: 'text-rose-600',
    countClass: 'text-rose-600',
    path: '/scene/0'
  },
  {
    key: 'chapter',
    label: '章節',
    count: allChapters.value.length,
    icon: 'fa-solid fa-book',
    bgClass: 'bg-violet-100 group-hover:bg-violet-200',
    iconClass: 'text-violet-600',
    countClass: 'text-violet-600',
    path: '/chapter/0'
  }
])

// Modules for quick entry cards
const modules = computed(() => [
  {
    path: '/worldbuilding',
    title: '世界觀規劃器',
    desc: '定義故事的世界背景、時代設定、魔法體系與規則',
    icon: 'fa-solid fa-globe',
    bgClass: 'bg-indigo-100 group-hover:bg-indigo-200',
    iconClass: 'text-indigo-600',
    count: allWorldbuildings.value.length
  },
  {
    path: '/character',
    title: '角色管理器',
    desc: '創造有血有肉的角色，設定性格、背景與外貌',
    icon: 'fa-solid fa-users',
    bgClass: 'bg-emerald-100 group-hover:bg-emerald-200',
    iconClass: 'text-emerald-600',
    count: allCharacters.value.length
  },
  {
    path: '/outline',
    title: '故事大綱生成器',
    desc: '從主題出發，AI 自動生成完整故事架構與章節大綱',
    icon: 'fa-solid fa-list',
    bgClass: 'bg-amber-100 group-hover:bg-amber-200',
    iconClass: 'text-amber-600',
    count: allOutlines.value.length
  },
  {
    path: '/scene/0',
    title: '場景規劃器',
    desc: '細化每章為場景，規劃劇情節奏與轉折',
    icon: 'fa-solid fa-clapperboard',
    bgClass: 'bg-rose-100 group-hover:bg-rose-200',
    iconClass: 'text-rose-600',
    count: allScenes.value.length
  },
  {
    path: '/chapter/0',
    title: '章節生成器',
    desc: 'AI 逐章生成完整小說內容，支援編輯與匯出',
    icon: 'fa-solid fa-book',
    bgClass: 'bg-violet-100 group-hover:bg-violet-200',
    iconClass: 'text-violet-600',
    count: allChapters.value.length
  }
])

const isAllEmpty = computed(() =>
  allWorldbuildings.value.length === 0 &&
  allCharacters.value.length === 0 &&
  allOutlines.value.length === 0 &&
  allScenes.value.length === 0 &&
  allChapters.value.length === 0
)

// Recent activity items (top 10 most recent across all modules)
const recentItems = computed(() => {
  const items = [
    ...allWorldbuildings.value.map(w => ({ type: 'worldbuilding', typeLabel: '世界觀', ...w, icon: 'fa-solid fa-globe', bgClass: 'bg-indigo-100', iconClass: 'text-indigo-600', path: '/worldbuilding', time: w.created_at || w.updated_at })),
    ...allCharacters.value.map(c => ({ type: 'character', typeLabel: '角色', ...c, icon: 'fa-solid fa-users', bgClass: 'bg-emerald-100', iconClass: 'text-emerald-600', path: '/character', time: c.created_at || c.updated_at })),
    ...allOutlines.value.map(o => ({ type: 'outline', typeLabel: '大綱', ...o, icon: 'fa-solid fa-list', bgClass: 'bg-amber-100', iconClass: 'text-amber-600', path: '/outline', time: o.created_at || o.updated_at })),
    ...allScenes.value.map(s => ({ type: 'scene', typeLabel: '場景', ...s, icon: 'fa-solid fa-clapperboard', bgClass: 'bg-rose-100', iconClass: 'text-rose-600', path: `/scene/${s.outline_id || 0}`, time: s.created_at || s.updated_at })),
    ...allChapters.value.map(c => ({ type: 'chapter', typeLabel: '章節', ...c, icon: 'fa-solid fa-book', bgClass: 'bg-violet-100', iconClass: 'text-violet-600', path: `/chapter/${c.outline_id || 0}`, time: c.created_at || c.updated_at }))
  ]
    .filter(item => item.time)
    .sort((a, b) => new Date(b.time) - new Date(a.time))
    .slice(0, 10)

  return items
})

function formatTime(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const now = new Date()
  const diffMs = now - d
  const diffMin = Math.floor(diffMs / 60000)
  const diffHr = Math.floor(diffMs / 3600000)
  const diffDay = Math.floor(diffMs / 86400000)

  if (diffMin < 1) return '剛剛'
  if (diffMin < 60) return `${diffMin} 分鐘前`
  if (diffHr < 24) return `${diffHr} 小時前`
  if (diffDay < 7) return `${diffDay} 天前`
  return `${d.getFullYear()}/${(d.getMonth() + 1).toString().padStart(2, '0')}/${d.getDate().toString().padStart(2, '0')}`
}

async function loadDashboard() {
  loading.value = true
  error.value = null

  try {
    // Step 1: Fetch all worldbuildings
    const wbRes = await api.getWorldbuildings()
    allWorldbuildings.value = wbRes.data || []
    const wbIds = allWorldbuildings.value.map(w => w.id).filter(Boolean)

    // Step 2: Parallel fetch characters & outlines for all worldbuildings
    if (wbIds.length > 0) {
      const [charResults, outlineResults] = await Promise.all([
        Promise.allSettled(wbIds.map(id => api.getCharacters(id))),
        Promise.allSettled(wbIds.map(id => api.getOutlines(id)))
      ])

      allCharacters.value = charResults
        .filter(r => r.status === 'fulfilled')
        .flatMap(r => r.value.data || [])

      allOutlines.value = outlineResults
        .filter(r => r.status === 'fulfilled')
        .flatMap(r => r.value.data || [])

      // Step 3: Parallel fetch scenes & chapters for all outlines
      const outlineIds = allOutlines.value.map(o => o.id).filter(Boolean)
      if (outlineIds.length > 0) {
        const [sceneResults, chapterResults] = await Promise.all([
          Promise.allSettled(outlineIds.map(id => api.getScenes(id))),
          Promise.allSettled(outlineIds.map(id => api.getChapters(id)))
        ])

        allScenes.value = sceneResults
          .filter(r => r.status === 'fulfilled')
          .flatMap(r => r.value.data || [])

        allChapters.value = chapterResults
          .filter(r => r.status === 'fulfilled')
          .flatMap(r => r.value.data || [])
      }
    }
  } catch (e) {
    console.error('Dashboard load failed:', e)
    error.value = e.response?.data?.detail || e.message || '未知錯誤'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadDashboard()
})
</script>
