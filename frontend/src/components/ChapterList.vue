<template>
  <div class="space-y-2">
    <h3 class="text-sm font-semibold text-gray-700 mb-3">章節列表</h3>

    <div v-if="!chapters.length" class="text-sm text-gray-400 py-4 text-center">
      尚無章節
    </div>

    <button
      v-for="(ch, idx) in chapters"
      :key="idx"
      @click="$emit('select', idx)"
      class="w-full text-left px-4 py-3 rounded-lg transition-colors text-sm"
      :class="selected === idx ? 'bg-indigo-50 border-2 border-indigo-300 text-indigo-900' : 'bg-white border border-gray-200 text-gray-700 hover:border-gray-300'"
    >
      <div class="flex items-center justify-between">
        <span class="font-medium">第{{ idx + 1 }}章 {{ ch.title }}</span>
        <span
          v-if="chapterStatus(idx)"
          class="text-xs px-1.5 py-0.5 rounded-full"
          :class="chapterStatus(idx) === 'completed' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'"
        >
          {{ chapterStatus(idx) === 'completed' ? '已生成' : '草稿' }}
        </span>
      </div>
      <p class="text-xs text-gray-400 mt-0.5 line-clamp-1">{{ ch.summary }}</p>
      <p v-if="chapterWordCount(idx)" class="text-xs text-gray-400 mt-1">字數：{{ chapterWordCount(idx) }}</p>
    </button>
  </div>
</template>

<script setup>
import { useChapterStore } from '../stores/chapter'

const props = defineProps({
  outlineId: { type: Number, required: true },
  chapters: { type: Array, default: () => [] },
  selected: { type: Number, default: null }
})

defineEmits(['select'])

const chapterStore = useChapterStore()

function chapterStatus(idx) {
  const ch = chapterStore.chapters[idx]
  return ch?.status || null
}

function chapterWordCount(idx) {
  const ch = chapterStore.chapters[idx]
  return ch?.content ? ch.content.length : 0
}
</script>
