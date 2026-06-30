<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">
        <font-awesome-icon icon="fa-solid fa-book" class="text-violet-600 mr-2" />
        {{ t('chapter.title') }}
      </h1>
      <div class="flex items-center space-x-4">
        <nav v-if="outline" class="flex items-center space-x-2 text-sm">
          <router-link :to="`/novel/${novelId}/outline`" class="text-violet-600 hover:text-violet-800">
            <font-awesome-icon icon="fa-solid fa-arrow-left" class="mr-1" />
            {{ t('chapter.backToOutline') }}
          </router-link>
          <span class="text-gray-300">|</span>
          <router-link
            :to="`/novel/${novelId}/scene/${outlineId}`"
            class="text-violet-600 hover:text-violet-800"
          >
            <font-awesome-icon icon="fa-solid fa-clapperboard" class="mr-1" />
            {{ t('chapter.scenePlanner') }}
          </router-link>
        </nav>
      </div>
    </div>

    <ErrorBanner v-if="chapterStore.error" :message="chapterStore.error" />

    <div v-if="outlineStore.loading" class="flex justify-center py-8">
      <font-awesome-icon icon="fa-solid fa-spinner" spin class="text-violet-600 text-2xl" />
    </div>

    <template v-if="outline">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-2">{{ outline.title }}</h2>
        <p class="text-gray-500 text-sm">{{ outline.description }}</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-1">
          <ChapterList
            :chapters="chapterTitles"
            :selected="selectedChapterTitle"
            @select="selectChapter"
          />
        </div>
        <div class="lg:col-span-2">
          <ChapterEditor
            v-if="selectedChapterTitle"
            :novel-id="novelId"
            :chapter-title="selectedChapterTitle"
          />
          <p v-else class="text-gray-400 text-center py-12">{{ t('chapter.selectChapterPrompt') }}</p>
        </div>
      </div>
    </template>
    <p v-else-if="!outlineStore.loading" class="text-gray-400 text-center py-8">{{ t('chapter.outlineNotFound') }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useOutlineStore } from '../stores/outline'
import { useChapterStore } from '../stores/chapter'
import ChapterList from '../components/ChapterList.vue'
import type { ChapterTitleData } from '../types'
import ChapterEditor from '../components/ChapterEditor.vue'
import ErrorBanner from '../components/ErrorBanner.vue'

const props = defineProps({
  novelId: { type: String, required: true },
  outlineId: { type: String, required: true }
})

const outlineStore = useOutlineStore()
const chapterStore = useChapterStore()
const { t } = useI18n()

const novelId = computed(() => Number.parseInt(props.novelId))
const outlineId = computed(() => Number.parseInt(props.outlineId))
const outline = computed(() => outlineStore.current)
const chapterTitles = computed(() => {
  return (outlineStore.current?.chapter_titles || []).sort((a, b) => a.idx - b.idx)
})
const selectedChapterTitle = ref<ChapterTitleData | null>(null)

onMounted(async () => {
  await outlineStore.fetchOne(outlineId.value)
  await chapterStore.fetchAll(outlineId.value)
  if (chapterTitles.value.length) {
    selectChapter(chapterTitles.value[0])
  }
})

function selectChapter(ct) {
  selectedChapterTitle.value = ct
}
</script>