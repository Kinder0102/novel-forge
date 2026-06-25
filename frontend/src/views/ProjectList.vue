<template>
  <div class="max-w-6xl mx-auto space-y-8 py-4">
    
    <section class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">{{ t('projects.title') }}</h1>
        <p class="text-gray-500 mt-1">{{ t('projects.subtitle') }}</p>
      </div>
      <button
        @click="showCreate = true"
        class="inline-flex items-center px-5 py-2.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium shadow-sm"
      >
        <font-awesome-icon icon="fa-solid fa-plus" class="mr-2" />
        {{ t('projects.createProject') }}
      </button>
    </section>

    
    <Form
      v-if="showCreate"
      :validation-schema="validationSchema"
      :initial-values="initialForm"
      @submit="handleCreate"
      class="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
    >
      <h2 class="text-lg font-semibold text-gray-900 mb-4">{{ t('projects.createNovel') }}</h2>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('projects.novelName') }} <span class="text-red-500">*</span></label>
          <Field name="title" v-slot="{ field, errorMessage }">
            <input
              v-bind="field"
              type="text"
              :placeholder="t('projects.novelNamePlaceholder')"
              class="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              :class="errorMessage ? 'border-red-400' : 'border-gray-300'"
            />
          </Field>
          <ErrorMessage name="title" class="text-red-500 text-xs mt-1" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('projects.description') }}</label>
          <Field name="description" v-slot="{ field }">
            <textarea
              v-bind="field"
              rows="3"
              :placeholder="t('projects.descriptionPlaceholder')"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            ></textarea>
          </Field>
        </div>
        <div class="flex space-x-3">
          <button type="submit" :disabled="novelStore.loading"
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors text-sm font-medium">
            <font-awesome-icon v-if="novelStore.loading" icon="fa-solid fa-spinner" spin class="mr-1.5" />
            {{ t('common.create') }}
          </button>
          <button type="button" @click="showCreate = false; resetForm()"
            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium">
            {{ t('common.cancel') }}
          </button>
        </div>
      </div>
    </Form>

    
    <div v-if="novelStore.error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4">{{ novelStore.error }}</div>

    
    <div v-if="novelStore.loading && novelStore.novels.length === 0" class="flex justify-center py-16">
      <font-awesome-icon icon="fa-solid fa-spinner" spin class="text-3xl text-indigo-500" />
    </div>

    
    <div v-else-if="novelStore.novels.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <router-link
        v-for="novel in novelStore.novels"
        :key="novel.id"
        :to="`/novel/${novel.id}`"
        class="group relative bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg hover:-translate-y-0.5 transition-all duration-300"
      >
        <div class="h-1.5 w-full" :class="statusBar(novel.status)"></div>

        <div class="p-6">
          <div class="flex items-start justify-between mb-4">
            <div class="w-10 h-10 rounded-xl flex items-center justify-center" :class="iconBg(novel.status)">
              <font-awesome-icon icon="fa-solid fa-feather" class="text-lg" :class="iconColor(novel.status)" />
            </div>
            <span class="text-xs px-2.5 py-1 rounded-full font-medium" :class="statusClass(novel.status)">
              {{ statusLabel(novel.status) }}
            </span>
          </div>

          <h2 class="text-base font-bold text-gray-900 mb-2 group-hover:text-indigo-600 transition-colors line-clamp-1">
            {{ novel.title }}
          </h2>

          <p class="text-sm text-gray-500 leading-relaxed line-clamp-3 mb-5">
            {{ novel.description || t('projects.noDescription') }}
          </p>

          <div class="flex items-center justify-between pt-4 border-t border-gray-50">
            <span class="text-xs text-gray-400 flex items-center">
              <font-awesome-icon icon="fa-solid fa-stopwatch" class="mr-1.5 text-[10px]" />
              {{ formatTime(novel.updated_at) }}
            </span>
            <span class="text-xs font-medium text-indigo-500 opacity-0 group-hover:opacity-100 transition-all duration-200 translate-x-1 group-hover:translate-x-0 flex items-center">
              {{ t('projects.enterProject') }}
              <font-awesome-icon icon="fa-solid fa-arrow-right" class="ml-1 text-[10px]" />
            </span>
          </div>
        </div>
      </router-link>
    </div>

    <div v-else class="text-center py-20 bg-white rounded-2xl shadow-sm border border-gray-100">
      <div class="w-16 h-16 mx-auto mb-5 rounded-2xl bg-indigo-50 flex items-center justify-center">
        <font-awesome-icon icon="fa-solid fa-feather" class="text-2xl text-indigo-400" />
      </div>
      <p class="text-gray-700 text-lg font-semibold mb-1">{{ t('projects.noNovels') }}</p>
      <p class="text-gray-400 text-sm">{{ t('projects.noNovelsDesc') }}</p>
    </div>
  </div>
</template><script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { Form, Field, ErrorMessage } from 'vee-validate'
import { toFormValidator } from '@vee-validate/zod'
import { useNovelStore } from '../stores/novel'
import { createNovelCreateSchema } from '../utils/validation'
import { formatTime } from '../utils/format'

const router = useRouter()
const novelStore = useNovelStore()
const { t } = useI18n()
const showCreate = ref(false)

const validationSchema = toFormValidator(createNovelCreateSchema())

const initialForm = ref({ title: '', description: '' })

function resetForm() {
  initialForm.value = { title: '', description: '' }
}

async function handleCreate(values) {
  const novel = await novelStore.create({ title: values.title.trim(), description: (values.description || '').trim() })
  if (novel) {
    resetForm()
    showCreate.value = false
    router.push(`/novel/${novel.id}`)
  }
}

function statusClass(s) {
  const map = { draft: 'bg-gray-100 text-gray-600', writing: 'bg-amber-100 text-amber-700', completed: 'bg-green-100 text-green-700' }
  return map[s] || 'bg-gray-100 text-gray-600'
}

function statusLabel(s) {
  const map = { draft: t('projects.statusDraft'), writing: t('projects.statusWriting'), completed: t('projects.statusCompleted') }
  return map[s] || s
}

function statusBar(s) {
  const map = { draft: 'bg-gray-300', writing: 'bg-amber-400', completed: 'bg-green-400' }
  return map[s] || 'bg-gray-300'
}

function iconBg(s) {
  const map = { draft: 'bg-gray-50', writing: 'bg-amber-50', completed: 'bg-green-50' }
  return map[s] || 'bg-gray-50'
}

function iconColor(s) {
  const map = { draft: 'text-gray-400', writing: 'text-amber-500', completed: 'text-green-500' }
  return map[s] || 'text-gray-400'
}

onMounted(() => { novelStore.fetchAll() })
</script>