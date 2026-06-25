<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 mb-6">
      <font-awesome-icon icon="fa-solid fa-clapperboard" class="text-indigo-600 mr-2" />
      Story Planner
    </h1>

    <div v-if="sceneStore.error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 mb-4">
      {{ sceneStore.error }}
    </div>

    <div v-if="outlineStore.loading" class="flex justify-center py-8">
      <font-awesome-icon icon="fa-solid fa-spinner" spin class="text-indigo-600 text-2xl" />
    </div>

    <template v-if="outline">
      <div class="bg-white rounded-xl shadow-md p-6 mb-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-2">{{ outline.title }}</h2>
        <p class="text-gray-500 text-sm">{{ outline.summary }}</p>
      </div>

      <!-- Chapter selector -->
      <div v-if="chapters.length" class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">選擇章節</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="(ch, idx) in chapters"
            :key="idx"
            @click="selectChapter(idx)"
            class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            :class="selectedChapter === idx ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
          >
            第{{ idx + 1 }}章 {{ ch.title }}
          </button>
        </div>
      </div>

      <template v-if="selectedChapter !== null">
        <SceneForm :outline-id="outlineId" :chapter-index="selectedChapter" />
        <SceneList :outline-id="outlineId" :chapter-index="selectedChapter" />
      </template>
      <p v-else-if="chapters.length" class="text-gray-400 text-center py-8">請選擇一個章節</p>
    </template>
    <p v-else-if="!outlineStore.loading" class="text-gray-400 text-center py-8">找不到此大綱</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useOutlineStore } from '../stores/outline'
import { useSceneStore } from '../stores/scene'
import SceneList from '../components/SceneList.vue'
import SceneForm from '../components/SceneForm.vue'

const route = useRoute()
const outlineStore = useOutlineStore()
const sceneStore = useSceneStore()

const outlineId = computed(() => parseInt(route.params.outlineId))
const outline = computed(() => outlineStore.current)
const chapters = computed(() => {
  if (!outlineStore.current?.chapters) return []
  if (typeof outlineStore.current.chapters === 'string') {
    try { return JSON.parse(outlineStore.current.chapters) } catch { return [] }
  }
  return outlineStore.current.chapters
})
const selectedChapter = ref(null)

onMounted(async () => {
  await outlineStore.fetchOne(outlineId.value)
  if (chapters.value.length) {
    selectChapter(0)
  }
})

function selectChapter(idx) {
  selectedChapter.value = idx
  sceneStore.fetchAll(outlineId.value, idx)
}
</script>
