<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">
        <font-awesome-icon icon="fa-solid fa-book" class="text-indigo-600 mr-2" />
        章節生成器
      </h1>
      <ExportButton v-if="outline" :outline-id="outlineId" />
    </div>

    <div v-if="chapterStore.error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 mb-4">
      {{ chapterStore.error }}
    </div>

    <div v-if="outlineStore.loading" class="flex justify-center py-8">
      <font-awesome-icon icon="fa-solid fa-spinner" spin class="text-indigo-600 text-2xl" />
    </div>

    <template v-if="outline">
      <div class="bg-white rounded-xl shadow-md p-6 mb-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-2">{{ outline.title }}</h2>
        <p class="text-gray-500 text-sm">{{ outline.summary }}</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-1">
          <ChapterList
            :outline-id="outlineId"
            :chapters="outlineChapters"
            :selected="selectedChapter"
            @select="selectChapter"
          />
        </div>
        <div class="lg:col-span-2">
          <ChapterEditor
            v-if="selectedChapter !== null"
            :outline-id="outlineId"
            :chapter="outlineChapters[selectedChapter]"
            :chapter-index="selectedChapter"
          />
          <p v-else class="text-gray-400 text-center py-12">請從左側選擇一個章節</p>
        </div>
      </div>
    </template>
    <p v-else-if="!outlineStore.loading" class="text-gray-400 text-center py-8">找不到此大綱</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useOutlineStore } from '../stores/outline'
import { useChapterStore } from '../stores/chapter'
import ChapterList from '../components/ChapterList.vue'
import ChapterEditor from '../components/ChapterEditor.vue'
import ExportButton from '../components/ExportButton.vue'

const route = useRoute()
const outlineStore = useOutlineStore()
const chapterStore = useChapterStore()

const outlineId = computed(() => parseInt(route.params.outlineId))
const outline = computed(() => outlineStore.current)
const outlineChapters = computed(() => {
  if (!outlineStore.current?.chapters) return []
  if (typeof outlineStore.current.chapters === 'string') {
    try { return JSON.parse(outlineStore.current.chapters) } catch { return [] }
  }
  return outlineStore.current.chapters
})
const selectedChapter = ref(null)

onMounted(async () => {
  await outlineStore.fetchOne(outlineId.value)
  chapterStore.fetchAll(outlineId.value)
  if (outlineChapters.value.length) {
    selectChapter(0)
  }
})

function selectChapter(idx) {
  selectedChapter.value = idx
}
</script>
