<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl font-semibold text-gray-900">
        {{ t('chapter.chapterNum', { n: chapterPosition + 1 }) }} {{ chapterTitle.title || '' }}
      </h2>
      <div class="flex items-center space-x-3">
        <span class="text-sm text-gray-400">{{ t('chapter.charCount', { count: wordCount }) }}</span>
        <button
          @click="saveChapter"
          :disabled="chapterStore.loading"
          class="bg-violet-600 hover:bg-violet-700 disabled:bg-violet-300 text-white rounded-lg px-4 py-2 text-sm font-medium transition-colors"
        >
          <font-awesome-icon icon="fa-solid fa-save" class="mr-1" />
          {{ t('chapter.save') }}
        </button>
      </div>
    </div>

    <div class="mb-6 rounded-lg border-l-4 border-violet-400 bg-gradient-to-r from-violet-50 to-white p-4">
      <div v-if="currentChapter?.content" class="mb-3 p-3 bg-amber-50 border border-amber-200 rounded-md">
        <div class="flex items-center justify-between mb-1">
          <p class="text-xs font-medium text-amber-600">{{ t('common.aiContent') }}</p>
          <button
            @click="regenSummary"
            :disabled="summaryLoading"
            class="text-xs text-amber-500 hover:text-amber-700 disabled:text-amber-300 transition-colors"
            :title="t('chapter.regenerateSummary')"
          >
            <font-awesome-icon
              :icon="summaryLoading ? 'fa-solid fa-spinner' : 'fa-solid fa-arrows-rotate'"
              :spin="summaryLoading"
            />
          </button>
        </div>
        <p v-if="currentChapter.summary" class="text-sm text-amber-900">{{ currentChapter.summary }}</p>
        <p v-else class="text-sm text-amber-400 italic">{{ t('chapter.noSummary') }}</p>
      </div>

      <div v-if="scenes.length" class="p-3 bg-white border border-gray-200 rounded-md">
        <p class="text-xs font-medium text-gray-500 mb-2">{{ t('chapter.sceneCount', { count: scenes.length }) }}</p>
        <div class="space-y-2">
          <div
            v-for="scene in scenes"
            :key="scene.id"
            class="text-sm text-gray-700 pb-2 border-b border-gray-100 last:border-0 last:pb-0"
          >
            <p class="font-medium text-gray-800">{{ scene.title || t('scene.sceneTitleWithNumber', { n: scene.scene_number }) }}</p>
            <p v-if="scene.description" class="text-xs mt-0.5 text-gray-500 whitespace-pre-wrap">{{ scene.description }}</p>
          </div>
        </div>
      </div>
      <p v-if="!currentChapter?.content && !scenes.length" class="text-xs text-gray-400">{{ t('chapter.noInfo') }}</p>
    </div>

    <div class="space-y-3 mb-4">
      <textarea
        v-model="description"
        class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-300 focus:border-violet-400 text-gray-600"
        rows="2"
        :placeholder="t('chapter.descriptionPlaceholder')"
      ></textarea>
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
        {{ t('chapter.aiGenerateContent') }}
      </button>
    </div>

    <textarea
      v-model="content"
      class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-violet-500 font-serif text-gray-800 leading-relaxed"
      rows="20"
      :placeholder="t('chapter.contentPlaceholder')"
    ></textarea>
  </div>
</template><script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useChapterStore } from '../stores/chapter'
import { useOutlineStore } from '../stores/outline'
import { useSceneStore } from '../stores/scene'

const props = defineProps({
  novelId: { type: Number, required: true },
  chapterTitle: { type: Object, required: true }
})

const { t } = useI18n()
const chapterStore = useChapterStore()
const outlineStore = useOutlineStore()
const sceneStore = useSceneStore()
const content = ref('')
const description = ref('')
const scenes = ref([])
const summaryLoading = ref(false)

const currentChapter = computed(() =>
  chapterStore.chapters.find(c => c.chapter_title_id === props.chapterTitle.id)
)

const sortedChapterTitles = computed(() =>
  [...(outlineStore.current?.chapter_titles || [])].sort((a, b) => a.idx - b.idx)
)
const chapterPosition = computed(() =>
  sortedChapterTitles.value.findIndex(ct => ct.id === props.chapterTitle.id)
)

async function fetchScenes() {
  try {
    await sceneStore.fetchAll(props.chapterTitle.id)
    scenes.value = sceneStore.scenes
  } catch {
    scenes.value = []
  }
}

watch(() => props.chapterTitle.id, () => {
  fetchScenes()
}, { immediate: true })

watch(currentChapter, (ch) => {
  content.value = ch?.content || ''
}, { immediate: true })

const wordCount = computed(() => content.value.length)

async function saveChapter() {
  if (chapterStore.loading) return
  const ch = chapterStore.chapters.find(c => c.chapter_title_id === props.chapterTitle.id)
  if (ch) {
    await chapterStore.update(ch.id, { content: content.value })
  } else {
    await chapterStore.create({
      chapter_title_id: props.chapterTitle.id,
      content: content.value
    })
  }
}

async function aiGenerate() {
  const result = await chapterStore.generateChapter({
    novel_id: props.novelId,
    worldbuilding_id: outlineStore.current.worldbuilding_id,
    chapter_title_id: props.chapterTitle.id,
    chapter_id: currentChapter.value?.id,
    description: description.value
  })

  if (result) {
    content.value = result.content || ''
    description.value = ''
  }
}

async function regenSummary() {
  const ch = currentChapter.value
  if (!ch) return
  summaryLoading.value = true
  try {
    await chapterStore.regenerateSummary(ch.id)
  } catch {
  } finally {
    summaryLoading.value = false
  }
}
</script>