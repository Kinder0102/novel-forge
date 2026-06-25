<template>
  <div class="space-y-2">
    <h3 class="text-sm font-semibold text-gray-700 mb-3">{{ t('chapter.chapterList') }}</h3>

    <div v-if="!chapters.length" class="text-sm text-gray-400 py-4 text-center">
      {{ t('chapter.noChapters') }}
    </div>

    <button
      v-for="(ch, idx) in chapters"
      :key="ch.id"
      @click="$emit('select', ch)"
      class="w-full text-left px-4 py-3 rounded-lg transition-colors text-sm"
      :class="selected?.id === ch.id ? 'bg-violet-50 border-2 border-violet-300 text-violet-900' : 'bg-white border border-gray-200 text-gray-700 hover:border-gray-300'"
    >
      <div class="flex items-center justify-between">
        <span class="font-medium">{{ t('chapter.chapterNum', { n: idx + 1 }) }} {{ ch.title }}</span>
        <span
          v-if="chapterStatus(ch.id)"
          class="text-xs px-1.5 py-0.5 rounded-full"
          :class="chapterStatus(ch.id) === 'completed' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'"
        >
          {{ chapterStatus(ch.id) === 'completed' ? t('chapter.statusGenerated') : t('chapter.statusDraft') }}
        </span>
      </div>
      <p class="text-xs text-gray-400 mt-0.5 line-clamp-1">{{ chapterContent(ch.id)?.description }}</p>
      <p v-if="chapterWordCount(ch.id)" class="text-xs text-gray-400 mt-1">{{ t('chapter.charCount', { count: chapterWordCount(ch.id) }) }}</p>
    </button>
  </div>
</template><script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useChapterStore } from '../stores/chapter'
import type { ChapterTitleData } from '../types'

const props = defineProps({
  chapters: { type: Array, default: () => [] },
  selected: { type: Object, default: null }
})

const emit = defineEmits<{ select: [ch: ChapterTitleData] }>()

const { t } = useI18n()
const chapterStore = useChapterStore()

function chapterContent(chapterTitleId) {
  return chapterStore.chapters.find(c => c.chapter_title_id === chapterTitleId)
}

function chapterStatus(chapterTitleId) {
  const ch = chapterContent(chapterTitleId)
  return ch?.status || null
}

function chapterWordCount(chapterTitleId) {
  const ch = chapterContent(chapterTitleId)
  return ch?.content ? ch.content.length : 0
}
</script>