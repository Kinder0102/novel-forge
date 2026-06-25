<template>
  <div class="bg-white rounded-xl shadow-md p-6">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl font-semibold text-gray-900">
        第{{ chapterIndex + 1 }}章 {{ chapter?.title || '' }}
      </h2>
      <div class="flex items-center space-x-3">
        <span class="text-sm text-gray-400">字數：{{ wordCount }}</span>
        <button
          @click="saveChapter"
          :disabled="chapterStore.loading"
          class="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white rounded-lg px-4 py-2 text-sm font-medium transition-colors"
        >
          <font-awesome-icon icon="fa-solid fa-save" class="mr-1" />
          儲存
        </button>
      </div>
    </div>

    <p class="text-sm text-gray-500 mb-4">{{ chapter?.summary || '' }}</p>

    <div class="mb-4">
      <button
        @click="aiGenerate"
        :disabled="chapterStore.loading"
        class="bg-gray-200 hover:bg-gray-300 disabled:bg-gray-100 text-gray-700 rounded-lg px-4 py-2 text-sm font-medium transition-colors"
      >
        <font-awesome-icon
          :icon="chapterStore.loading ? 'fa-solid fa-spinner' : 'fa-solid fa-magic-wand-sparkles'"
          :spin="chapterStore.loading"
          class="mr-1"
        />
        AI 生成內容
      </button>
    </div>

    <textarea
      v-model="content"
      class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 font-serif text-gray-800 leading-relaxed"
      rows="20"
      placeholder="章節內容…"
    ></textarea>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useChapterStore } from '../stores/chapter'
import { useOutlineStore } from '../stores/outline'

const props = defineProps({
  outlineId: { type: Number, required: true },
  chapter: { type: Object, default: null },
  chapterIndex: { type: Number, required: true }
})

const chapterStore = useChapterStore()
const outlineStore = useOutlineStore()
const content = ref('')

watch(() => props.chapterIndex, () => {
  const ch = chapterStore.chapters[props.chapterIndex]
  content.value = ch?.content || ''
})

const wordCount = computed(() => content.value.length)

async function saveChapter() {
  const ch = chapterStore.chapters[props.chapterIndex]
  if (ch) {
    await chapterStore.update(ch.id, { content: content.value })
  } else {
    await chapterStore.create({
      outline_id: props.outlineId,
      chapter_index: props.chapterIndex,
      title: props.chapter?.title || '',
      content: content.value
    })
  }
}

async function aiGenerate() {
  const outline = outlineStore.current
  const context = outline ? `世界觀：${outline.title}\n${outline.summary}` : ''

  const result = await chapterStore.generateChapter({
    outline_id: props.outlineId,
    chapter_index: props.chapterIndex,
    chapter_title: props.chapter?.title || '',
    chapter_summary: props.chapter?.summary || '',
    context
  })

  if (result) {
    content.value = result.content || ''
  }
}
</script>
