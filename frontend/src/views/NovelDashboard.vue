<template>
  <div class="max-w-6xl mx-auto">
    
    <div v-if="loading" class="flex justify-center py-20">
      <font-awesome-icon icon="fa-solid fa-spinner" class="animate-spin text-3xl text-indigo-500" />
    </div>

    
    <ErrorBanner v-else-if="error" :message="error" />

    
    <div v-else class="space-y-8">
      
      <section class="grid grid-cols-2 md:grid-cols-5 gap-4">
        <router-link
          v-for="s in stats" :key="s.key" :to="s.path"
          class="rounded-xl border border-gray-200 p-4 flex flex-col justify-between transition-all duration-150"
          :class="{
            'bg-white hover:bg-indigo-50/30': s.key === 'worldbuilding',
            'bg-white hover:bg-emerald-50/30': s.key === 'character',
            'bg-white hover:bg-amber-50/30': s.key === 'outline',
            'bg-white hover:bg-rose-50/30': s.key === 'scene',
            'bg-white hover:bg-violet-50/30': s.key === 'chapter',
          }"
        >
          <div class="flex items-center space-x-2 mb-3">
            <div class="w-8 h-8 rounded-lg flex items-center justify-center"
              :class="{
                'bg-indigo-100': s.key === 'worldbuilding',
                'bg-emerald-100': s.key === 'character',
                'bg-amber-100': s.key === 'outline',
                'bg-rose-100': s.key === 'scene',
                'bg-violet-100': s.key === 'chapter',
              }"
            >
              <font-awesome-icon :icon="s.icon"
                :class="{
                  'text-indigo-600': s.key === 'worldbuilding',
                  'text-emerald-600': s.key === 'character',
                  'text-amber-600': s.key === 'outline',
                  'text-rose-600': s.key === 'scene',
                  'text-violet-600': s.key === 'chapter',
                }"
                class="text-sm"
              />
            </div>
            <span class="text-xs font-semibold text-gray-600">{{ s.label }}</span>
          </div>
          <p :class="{
            'text-indigo-600': s.key === 'worldbuilding',
            'text-emerald-600': s.key === 'character',
            'text-amber-600': s.key === 'outline',
            'text-rose-600': s.key === 'scene',
            'text-violet-600': s.key === 'chapter',
          }" class="text-2xl font-bold mb-0.5">{{ s.count }}</p>
          <p class="text-xs text-gray-400">{{ s.subtitle }}</p>
          <div class="mt-3 w-full h-1 rounded-full bg-gray-100">
            <div
              :class="{
                'bg-indigo-500': s.key === 'worldbuilding',
                'bg-emerald-500': s.key === 'character',
                'bg-amber-500': s.key === 'outline',
                'bg-rose-500': s.key === 'scene',
                'bg-violet-500': s.key === 'chapter',
              }"
              class="h-1 rounded-full"
              :style="{ width: (s.count ? '100%' : '0%') }"
            ></div>
          </div>
        </router-link>
      </section>

      
      <section>
        <Form
          :validation-schema="validationSchema"
          :initial-values="writingStyleInitial"
          @submit="saveWritingStyle"
          class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6"
        >
          <h2 class="text-lg font-semibold text-gray-900 mb-1 flex items-center space-x-2">
            <font-awesome-icon icon="fa-solid fa-pen-fancy" class="text-indigo-500" />
            <span>{{ t('dashboard.writingStyle') }}</span>
          </h2>
          <p class="text-sm text-gray-400 mb-3">{{ t('dashboard.writingStyleDesc') }}</p>
          <Field name="writing_style" v-slot="{ field }">
            <textarea
              v-bind="field"
              rows="3"
              :placeholder="t('dashboard.writingStylePlaceholder')"
              class="border border-gray-300 rounded-lg px-3 py-2 w-full focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-vertical text-sm"
            ></textarea>
          </Field>
          <div class="mt-3 flex items-center space-x-3">
            <button
              type="submit"
              :disabled="savingWritingStyle"
              class="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors disabled:opacity-50 text-sm"
            >
              <font-awesome-icon v-if="savingWritingStyle" icon="fa-solid fa-spinner" class="animate-spin" />
              <span>{{ t('common.save') }}</span>
            </button>
            <span v-if="writingStyleSaved" class="text-green-600 text-sm font-medium">
              <font-awesome-icon icon="fa-solid fa-check" class="mr-1" />{{ t('common.saveSuccess') }}
            </span>
          </div>
        </Form>
      </section>

      
      <div v-if="isAllEmpty" class="text-center py-16 bg-white rounded-2xl shadow-sm border border-gray-200">
        <div class="w-16 h-16 rounded-2xl bg-indigo-50 flex items-center justify-center mx-auto mb-5">
          <font-awesome-icon icon="fa-solid fa-feather" class="text-2xl text-indigo-400" />
        </div>
        <p class="text-gray-500 text-lg mb-1">{{ t('dashboard.noCreationData') }}</p>
        <p class="text-gray-400 text-sm mb-6">{{ t('dashboard.noCreationDataDesc') }}</p>
        <router-link
          :to="`/novel/${novelId}/worldbuilding`"
          class="inline-flex items-center px-5 py-2.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium shadow-sm"
        >
          <font-awesome-icon icon="fa-solid fa-plus" class="mr-2" />{{ t('dashboard.createWorldbuilding') }}
        </router-link>
      </div>

      
      <section v-if="allChapters.length" class="bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden">
        <div class="bg-indigo-50 px-6 py-3 border-b border-indigo-100">
          <h2 class="text-sm font-semibold text-indigo-800 flex items-center space-x-2">
            <font-awesome-icon icon="fa-solid fa-book-open" />
            <span>{{ t('dashboard.chapterList') }}</span>
          </h2>
        </div>
        <div class="px-6 py-4 divide-y divide-gray-100">
          <div v-for="group in chapterGroups" :key="group.outlineId" class="py-3 first:pt-1">
            <p class="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide">{{ group.outlineTitle }}</p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-1.5">
              <router-link
                v-for="(ch, ix) in group.chapters"
                :key="ch.id"
                :to="`/novel/${novelId}/read/${group.outlineId}/${ch.ctId}`"
                class="flex items-center justify-between px-3 py-2 rounded-lg text-sm hover:bg-indigo-50 transition-colors group"
              >
                <span class="text-gray-700 group-hover:text-indigo-700 truncate">
                  <span class="text-gray-400 text-xs mr-1.5">{{ ix + 1 }}.</span>
                  {{ ch.title || t('common.untitled') }}
                </span>
              </router-link>
            </div>
          </div>
        </div>
      </section>

      
      <section class="border border-red-200 rounded-2xl overflow-hidden">
        <div class="bg-red-50 px-6 py-3 border-b border-red-200">
          <h2 class="text-sm font-semibold text-red-800 flex items-center space-x-2">
            <font-awesome-icon icon="fa-solid fa-triangle-exclamation" />
            <span>{{ t('dashboard.dangerZone') }}</span>
          </h2>
        </div>
        <div class="bg-white px-6 py-5">
          <p class="text-sm text-gray-600 mb-1"><strong>{{ t('dashboard.deleteProject') }}</strong></p>
          <p class="text-xs text-gray-400 mb-4">
            {{ t('dashboard.deleteWarning') }}
          </p>

          
          <button
            v-if="!showDeleteConfirm"
            @click="showDeleteConfirm = true"
            class="px-4 py-2 border border-red-300 text-red-600 rounded-lg text-sm font-medium hover:bg-red-50 transition-colors"
          >
            <font-awesome-icon icon="fa-solid fa-trash" class="mr-2" />{{ t('dashboard.deleteProject') }}
          </button>

          
          <div v-else class="border border-red-300 rounded-lg p-4 bg-red-50/30">
            <p class="text-sm text-gray-700 mb-3">
              {{ t('dashboard.deleteConfirmText', { name: novelTitle }) }}
            </p>
            <div class="flex items-center space-x-3">
              <input
                v-model="deleteConfirmText"
                type="text"
                :placeholder="novelTitle"
                class="border border-gray-300 rounded-lg px-3 py-2 text-sm w-64 focus:ring-2 focus:ring-red-500 focus:border-red-500"
                @keydown.enter.prevent="executeDelete"
              />
              <button
                @click="executeDelete"
                :disabled="deleteConfirmText !== novelTitle || deleting"
                class="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
              >
                <font-awesome-icon v-if="deleting" icon="fa-solid fa-spinner" class="animate-spin mr-2" />
                <span>{{ t('dashboard.confirmDelete') }}</span>
              </button>
              <button
                @click="cancelDelete"
                :disabled="deleting"
                class="px-4 py-2 border border-gray-300 text-gray-600 rounded-lg text-sm hover:bg-gray-50 transition-colors"
              >
                {{ t('common.cancel') }}
              </button>
            </div>
            <p v-if="deleteError" class="text-red-600 text-xs mt-2">{{ deleteError }}</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template><script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { extractErrorMessage } from '../utils/error'
import { Form, Field } from 'vee-validate'
import { toFormValidator } from '@vee-validate/zod'
import { useNovelStore } from '../stores/novel'
import { useWorldbuildingStore } from '../stores/worldbuilding'
import { useCharacterStore } from '../stores/character'
import { useOutlineStore } from '../stores/outline'
import { useSceneStore } from '../stores/scene'
import { useChapterStore } from '../stores/chapter'
import { createNovelUpdateSchema } from '../utils/validation'
import { useNovelStats } from '../composables/useNovelStats'
import { useChapterGroups } from '../composables/useChapterGroups'
import ErrorBanner from '../components/ErrorBanner.vue'

const props = defineProps({ novelId: { type: String, required: true } })
const router = useRouter()
const novelStore = useNovelStore()
const worldbuildingStore = useWorldbuildingStore()
const characterStore = useCharacterStore()
const outlineStore = useOutlineStore()
const sceneStore = useSceneStore()
const chapterStore = useChapterStore()
const { t } = useI18n()

const validationSchema = toFormValidator(createNovelUpdateSchema())
const loading = ref(true)
const error = ref(null)
const novelTitle = ref('')
const writingStyleInitial = ref({ writing_style: '' })
const savingWritingStyle = ref(false)
const writingStyleSaved = ref(false)

const showDeleteConfirm = ref(false)
const deleteConfirmText = ref('')
const deleting = ref(false)
const deleteError = ref<string | null>(null)

const baseUrl = computed(() => `/novel/${props.novelId}`)

const { stats } = useNovelStats(
  baseUrl,
  computed(() => worldbuildingStore.worldbuildings.length),
  computed(() => characterStore.characters.length),
  computed(() => outlineStore.outlines.length),
  computed(() => sceneStore.scenes.length),
  computed(() => chapterStore.chapters.length),
)

const allOutlines = computed(() => outlineStore.outlines)
const allChapters = computed(() => chapterStore.chapters)
const allChapterTitles = computed(() => (outlineStore.outlines || []).flatMap((o) => o?.chapter_titles || []))

const isAllEmpty = computed(
  () =>
    worldbuildingStore.worldbuildings.length === 0 &&
    characterStore.characters.length === 0 &&
    outlineStore.outlines.length === 0 &&
    sceneStore.scenes.length === 0 &&
    chapterStore.chapters.length === 0,
)

const { chapterGroups } = useChapterGroups(allOutlines, computed(() => chapterStore.chapters), allChapterTitles)

async function loadDashboard() {
  loading.value = true
  error.value = null
  try {
    const novelIdNum = parseInt(props.novelId)
    await novelStore.fetchOne(novelIdNum)
    const novel = novelStore.current
    novelTitle.value = novel?.title ?? ''
    writingStyleInitial.value = { writing_style: novel?.writing_style || '' }

    await Promise.all([
      worldbuildingStore.fetchAll(novelIdNum),
      characterStore.fetchAll({ novelId: novelIdNum }),
      outlineStore.fetchAll({ novelId: novelIdNum }),
    ])

    const outlineIds = outlineStore.outlines.map((o) => o.id).filter(Boolean)
    if (outlineIds.length) {
      await Promise.all([
        sceneStore.loadAllForOutlines(outlineIds),
        chapterStore.loadAllForOutlines(outlineIds),
      ])
    }
  } catch (e) {
    error.value = extractErrorMessage(e)
  } finally {
    loading.value = false
  }
}

async function saveWritingStyle(values) {
  savingWritingStyle.value = true
  writingStyleSaved.value = false
  try {
    await novelStore.update(parseInt(props.novelId), { writing_style: values.writing_style || '' })
    writingStyleInitial.value = { writing_style: values.writing_style || '' }
    writingStyleSaved.value = true
    setTimeout(() => { writingStyleSaved.value = false }, 2000)
  } catch (e) {
    console.error('Save writing style failed:', e)
  } finally { savingWritingStyle.value = false }
}

async function executeDelete() {
  if (deleteConfirmText.value !== novelTitle.value || deleting.value) return
  deleting.value = true
  deleteError.value = null
  try {
    await novelStore.remove(parseInt(props.novelId))
    router.push('/')
  } catch (e) {
    deleteError.value = extractErrorMessage(e)
    deleting.value = false
  }
}

function cancelDelete() {
  showDeleteConfirm.value = false
  deleteConfirmText.value = ''
  deleteError.value = null
}

onMounted(() => { loadDashboard() })
</script>