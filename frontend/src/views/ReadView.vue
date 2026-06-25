<template>
  <div class="max-w-3xl mx-auto">
    
    <div v-if="loading" class="flex justify-center py-20">
      <font-awesome-icon icon="fa-solid fa-spinner" class="animate-spin text-3xl text-indigo-500" />
    </div>

    
    <ErrorBanner v-else-if="error" :message="error" />

    
    <template v-else-if="chapter">
      
      <div class="flex items-center justify-between mb-8 pb-4 border-b border-gray-200">
        <router-link
          :to="`/novel/${novelId}`"
          class="text-sm text-gray-400 hover:text-gray-600 transition-colors flex items-center space-x-1"
        >
          <font-awesome-icon icon="fa-solid fa-arrow-left" />
          <span>{{ t('read.backToCatalog') }}</span>
        </router-link>
        <span class="text-xs text-gray-400">{{ outline?.title || '' }}</span>
      </div>

      
      <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ chapter.title }}</h1>
      <p class="text-sm text-gray-400 mb-10">{{ t('read.chapterNum', { n: currentPos + 1 }) }}</p>

      
      <article class="prose prose-lg prose-indigo max-w-none leading-relaxed text-gray-800">
        <p
          v-for="(para, i) in paragraphs"
          :key="i"
          class="mb-4"
        >{{ para }}</p>
      </article>

      
      <div class="mt-12 pt-6 border-t border-gray-200 flex items-center justify-between">
        <button
          v-if="hasPrev"
          @click="goTo(sortedTitles[currentPos - 1].id)"
          class="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50 hover:border-gray-400 transition-colors"
        >
          <font-awesome-icon icon="fa-solid fa-chevron-left" class="text-xs" />
          <span>{{ t('read.prevChapter') }}</span>
        </button>
        <span v-else class="w-24"></span>

        <span class="text-xs text-gray-400">{{ currentPos + 1 }} / {{ sortedTitles.length }}</span>

        <button
          v-if="hasNext"
          @click="goTo(sortedTitles[currentPos + 1].id)"
          class="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50 hover:border-gray-400 transition-colors"
        >
          <span>{{ t('read.nextChapter') }}</span>
          <font-awesome-icon icon="fa-solid fa-chevron-right" class="text-xs" />
        </button>
        <span v-else class="w-24"></span>
      </div>
    </template>

    <p v-else class="text-gray-400 text-center py-8">{{ t('read.chapterNotFound') }}</p>
  </div>
<template v-else-if="chapter">
      
      <div class="flex items-center justify-between mb-8 pb-4 border-b border-gray-200">
        <router-link
          :to="`/novel/${novelId}`"
          class="text-sm text-gray-400 hover:text-gray-600 transition-colors flex items-center space-x-1"
        >
          <font-awesome-icon icon="fa-solid fa-arrow-left" />
          <span>{{ t('read.backToCatalog') }}</span>
        </router-link>
        <span class="text-xs text-gray-400">{{ outline?.title || '' }}</span>
      </div>

      
      <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ chapter.title }}</h1>
      <p class="text-sm text-gray-400 mb-10">{{ t('read.chapterNum', { n: currentPos + 1 }) }}</p>

      
      <article class="prose prose-lg prose-indigo max-w-none leading-relaxed text-gray-800">
        <p
          v-for="(para, i) in paragraphs"
          :key="i"
          class="mb-4"
        >{{ para }}</p>
      </article>

      
      <div class="mt-12 pt-6 border-t border-gray-200 flex items-center justify-between">
        <button
          v-if="hasPrev"
          @click="goTo(sortedTitles[currentPos - 1].id)"
          class="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50 hover:border-gray-400 transition-colors"
        >
          <font-awesome-icon icon="fa-solid fa-chevron-left" class="text-xs" />
          <span>{{ t('read.prevChapter') }}</span>
        </button>
        <span v-else class="w-24"></span>

        <span class="text-xs text-gray-400">{{ currentPos + 1 }} / {{ sortedTitles.length }}</span>

        <button
          v-if="hasNext"
          @click="goTo(sortedTitles[currentPos + 1].id)"
          class="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50 hover:border-gray-400 transition-colors"
        >
          <span>{{ t('read.nextChapter') }}</span>
          <font-awesome-icon icon="fa-solid fa-chevron-right" class="text-xs" />
        </button>
        <span v-else class="w-24"></span>
      </div>
    </template></template><script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useOutlineStore } from '../stores/outline'
import { useChapterStore } from '../stores/chapter'
import ErrorBanner from '../components/ErrorBanner.vue'
import { extractErrorMessage } from '../utils/error'
import type { ChapterContent } from '../stores/chapter'

const { t } = useI18n()

const props = defineProps({
  novelId: { type: String, required: true },
  outlineId: { type: String, required: true },
  chapterTitleId: { type: String, default: '' }
})

const router = useRouter()
const outlineStore = useOutlineStore()
const chapterStore = useChapterStore()

const loading = ref(true)
const error = ref<string | null>(null)
const chapter = ref<ChapterContent | null>(null)
const outline = ref<any>(null)
const chapterTitles = ref<any[]>([])

const sortedTitles = computed(() =>
  [...chapterTitles.value].sort((a: any, b: any) => a.idx - b.idx)
)

const chapterTitle = computed(() =>
  chapterTitles.value.find((ct: any) => ct.id === chapter.value?.chapter_title_id)
)

const currentPos = computed(() =>
  chapter.value ? sortedTitles.value.findIndex((ct: any) => ct.id === chapter.value!.chapter_title_id) : -1
)

const hasPrev = computed(() => currentPos.value > 0)

const hasNext = computed(() =>
  currentPos.value >= 0 && currentPos.value < sortedTitles.value.length - 1
)

const paragraphs = computed(() => {
  if (!chapter.value?.content) return []
  return chapter.value.content.split('\n').filter((p: string) => p.trim())
})

function goTo(chapterTitleId: number) {
  router.push(`/novel/${props.novelId}/read/${props.outlineId}/${chapterTitleId}`)
}

async function load() {
  loading.value = true
  error.value = null
  try {
    const oid = parseInt(props.outlineId)
    const ctId = parseInt(props.chapterTitleId) || null

    
    await outlineStore.fetchOne(oid)
    await chapterStore.fetchAll(oid)

    outline.value = outlineStore.current
    chapterTitles.value = outlineStore.current?.chapter_titles || []

    const chaptersData = chapterStore.chapters.filter((c, i, arr) => {
      return arr.findIndex((x) => x.chapter_title_id === c.chapter_title_id) === i
    })

    if (ctId) {
      const found = chaptersData.find((c) => c.chapter_title_id === ctId)
      chapter.value = found || chaptersData[0] || null
    } else if (chaptersData.length > 0) {
      chapter.value = chaptersData[0]
    } else {
      chapter.value = null
    }
  } catch (e: any) {
    error.value = e.response?.data?.detail || e.message || t('common.loadFailed')
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => props.chapterTitleId, load)
</script>