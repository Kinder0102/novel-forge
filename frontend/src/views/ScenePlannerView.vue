<template>
  <div>
    
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">
        <font-awesome-icon icon="fa-solid fa-clapperboard" class="text-rose-600 mr-2" />
        {{ t('scene.title') }}
      </h1>
      
      <nav v-if="outline" class="flex items-center space-x-2 text-sm">
        <router-link :to="`/novel/${novelId}/outline`" class="text-rose-600 hover:text-rose-800">
          <font-awesome-icon icon="fa-solid fa-arrow-left" class="mr-1" />
          {{ t('scene.backToOutline') }}
        </router-link>
        <span class="text-gray-300">|</span>
        <router-link
          :to="`/novel/${novelId}/chapter/${outlineId}`"
          class="text-rose-600 hover:text-rose-800"
        >
          <font-awesome-icon icon="fa-solid fa-book-open" class="mr-1" />
          {{ t('scene.chapterEditor') }}
        </router-link>
      </nav>
    </div>

    
    <ErrorBanner v-if="sceneStore.error" :message="sceneStore.error" />

    
    <div v-if="outlineStore.loading" class="flex justify-center py-8">
      <font-awesome-icon icon="fa-solid fa-spinner" spin class="text-rose-600 text-2xl" />
    </div>

    <template v-if="outline">
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-2">{{ outline.title }}</h2>
        <p class="text-gray-500 text-sm">{{ outline.summary }}</p>
      </div>

      
      <div v-if="chapterTitles.length" class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('scene.selectChapter') }}</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="(ct, ix) in chapterTitles"
            :key="ct.id"
            @click="selectChapter(ct)"
            class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            :class="selectedChapter?.id === ct.id ? 'bg-rose-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
          >
            {{ t('chapter.chapterNum', { n: ix + 1 }) }} {{ ct.title }}
          </button>
        </div>
      </div>

      
      <div
        v-if="selectedChapter"
        class="flex items-center space-x-3 mb-4 text-sm text-gray-500"
      >
        <font-awesome-icon icon="fa-solid fa-clapperboard" class="text-rose-400" />
        <span>
          {{ t('scene.currentChapter') }}
          <span class="font-medium text-gray-700">{{ selectedChapter.title }}</span>
        </span>
        <span v-if="!sceneStore.loading" class="text-gray-300">|</span>
        <span v-if="!sceneStore.loading">{{ t('scene.sceneCount', { count: sceneStore.scenes.length }) }}</span>
      </div>

      <template v-if="selectedChapter">
        <SceneForm
          ref="formRef"
          :novel-id="novelId"
          :chapter-title-id="selectedChapter.id"
        />
        <SceneList
          :chapter-title-id="selectedChapter.id"
          @edit-scene="onEditScene"
        />
      </template>
      <p v-else-if="chapterTitles.length" class="text-gray-400 text-center py-8">{{ t('scene.selectChapterPrompt') }}</p>
      <p v-else class="text-gray-400 text-center py-8">
        <font-awesome-icon icon="fa-solid fa-circle-info" class="text-3xl mb-2 block" />
        {{ t('scene.noChapterPrompt') }}
      </p>
    </template>
    <p v-else-if="!outlineStore.loading" class="text-gray-400 text-center py-8">{{ t('scene.outlineNotFound') }}</p>
  </div>
</template>
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import type { ChapterTitleData } from '../types'
import { useOutlineStore } from '../stores/outline'
import { useSceneStore } from '../stores/scene'
import { useChapterStore } from '../stores/chapter'
import ErrorBanner from '../components/ErrorBanner.vue'
import SceneList from '../components/SceneList.vue'
import SceneForm from '../components/SceneForm.vue'

const props = defineProps({
  novelId: { type: String, required: true },
  outlineId: { type: String, required: true }
})

const route = useRoute()
const outlineStore = useOutlineStore()
const sceneStore = useSceneStore()
const chapterStore = useChapterStore()
const { t } = useI18n()

const novelId = computed(() => Number.parseInt(props.novelId))
const outlineId = computed(() => Number.parseInt(props.outlineId))
const outline = computed(() => outlineStore.current)
const chapterTitles = computed(() => {
  return (outlineStore.current?.chapter_titles || []).sort((a, b) => a.idx - b.idx)
})
const selectedChapter = ref<ChapterTitleData | null>(null)
const formRef = ref<any>(null)

onMounted(async () => {
  await outlineStore.fetchOne(outlineId.value)
  if (chapterTitles.value.length) {
    selectChapter(chapterTitles.value[0])
  }
})

function selectChapter(ct) {
  selectedChapter.value = ct
  sceneStore.fetchAll(ct.id)
}

function onEditScene(scene) {
  formRef.value?.startEdit(scene)
}
</script>