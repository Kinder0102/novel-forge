<template>
  <div class="max-w-4xl mx-auto space-y-12 py-4">
    
    <section class="text-center space-y-4">
      <h1 class="text-4xl font-extrabold text-gray-900 tracking-tight">NovelForge</h1>
      <p class="text-lg text-gray-500 max-w-2xl mx-auto leading-relaxed">
        {{ t('landing.heroDesc') }}
      </p>
      <router-link
        to="/projects"
        class="inline-flex items-center px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium shadow-sm"
      >
        <font-awesome-icon icon="fa-solid fa-play" class="mr-2" />
        {{ t('landing.startCreating') }}
      </router-link>
    </section>

    
    <section>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div
          class="group bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-indigo-200 transition-all duration-200"
        >
          <div class="w-10 h-10 rounded-lg bg-indigo-50 flex items-center justify-center mb-4 group-hover:bg-indigo-100 transition-colors">
            <font-awesome-icon icon="fa-solid fa-globe" class="text-xl text-indigo-500" />
          </div>
          <h2 class="text-lg font-semibold text-gray-900 mb-2">{{ t('landing.worldbuildingTitle') }}</h2>
          <p class="text-sm text-gray-500 leading-relaxed">
            {{ t('landing.worldbuildingDesc') }}
          </p>
        </div>

        <div
          class="group bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-emerald-200 transition-all duration-200"
        >
          <div class="w-10 h-10 rounded-lg bg-emerald-50 flex items-center justify-center mb-4 group-hover:bg-emerald-100 transition-colors">
            <font-awesome-icon icon="fa-solid fa-user" class="text-xl text-emerald-500" />
          </div>
          <h2 class="text-lg font-semibold text-gray-900 mb-2">{{ t('landing.characterTitle') }}</h2>
          <p class="text-sm text-gray-500 leading-relaxed">
            {{ t('landing.characterDesc') }}
          </p>
        </div>

        <div
          class="group bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-amber-200 transition-all duration-200"
        >
          <div class="w-10 h-10 rounded-lg bg-amber-50 flex items-center justify-center mb-4 group-hover:bg-amber-100 transition-colors">
            <font-awesome-icon icon="fa-solid fa-list-ol" class="text-xl text-amber-500" />
          </div>
          <h2 class="text-lg font-semibold text-gray-900 mb-2">{{ t('landing.outlineTitle') }}</h2>
          <p class="text-sm text-gray-500 leading-relaxed">
            {{ t('landing.outlineDesc') }}
          </p>
        </div>

        <div
          class="group bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-rose-200 transition-all duration-200"
        >
          <div class="w-10 h-10 rounded-lg bg-rose-50 flex items-center justify-center mb-4 group-hover:bg-rose-100 transition-colors">
            <font-awesome-icon icon="fa-solid fa-clapperboard" class="text-xl text-rose-500" />
          </div>
          <h2 class="text-lg font-semibold text-gray-900 mb-2">{{ t('landing.sceneTitle') }}</h2>
          <p class="text-sm text-gray-500 leading-relaxed">
            {{ t('landing.sceneDesc') }}
          </p>
        </div>

        <div
          class="group bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-violet-200 transition-all duration-200"
        >
          <div class="w-10 h-10 rounded-lg bg-violet-50 flex items-center justify-center mb-4 group-hover:bg-violet-100 transition-colors">
            <font-awesome-icon icon="fa-solid fa-book-open" class="text-xl text-violet-500" />
          </div>
          <h2 class="text-lg font-semibold text-gray-900 mb-2">{{ t('landing.chapterTitle') }}</h2>
          <p class="text-sm text-gray-500 leading-relaxed">
            {{ t('landing.chapterDesc') }}
          </p>
        </div>
      </div>
    </section>

    
    <section class="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
      <h2 class="text-xl font-semibold text-gray-900 text-center mb-8">{{ t('landing.workflowTitle') }}</h2>
      <div class="grid grid-cols-1 sm:grid-cols-5 gap-4">
        <div class="text-center">
          <div class="w-10 h-10 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center mx-auto mb-3 font-bold text-sm">1</div>
          <p class="text-sm font-medium text-gray-900">{{ t('landing.workflowStep1') }}</p>
          <p class="text-xs text-gray-500 mt-1">{{ t('landing.workflowStep1Desc') }}</p>
        </div>
        <div class="text-center">
          <div class="w-10 h-10 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto mb-3 font-bold text-sm">2</div>
          <p class="text-sm font-medium text-gray-900">{{ t('landing.workflowStep2') }}</p>
          <p class="text-xs text-gray-500 mt-1">{{ t('landing.workflowStep2Desc') }}</p>
        </div>
        <div class="text-center">
          <div class="w-10 h-10 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center mx-auto mb-3 font-bold text-sm">3</div>
          <p class="text-sm font-medium text-gray-900">{{ t('landing.workflowStep3') }}</p>
          <p class="text-xs text-gray-500 mt-1">{{ t('landing.workflowStep3Desc') }}</p>
        </div>
        <div class="text-center">
          <div class="w-10 h-10 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center mx-auto mb-3 font-bold text-sm">4</div>
          <p class="text-sm font-medium text-gray-900">{{ t('landing.workflowStep4') }}</p>
          <p class="text-xs text-gray-500 mt-1">{{ t('landing.workflowStep4Desc') }}</p>
        </div>
        <div class="text-center">
          <div class="w-10 h-10 rounded-full bg-violet-100 text-violet-600 flex items-center justify-center mx-auto mb-3 font-bold text-sm">5</div>
          <p class="text-sm font-medium text-gray-900">{{ t('landing.workflowStep5') }}</p>
          <p class="text-xs text-gray-500 mt-1">{{ t('landing.workflowStep5Desc') }}</p>
        </div>
      </div>
    </section>

    
    <section class="bg-gradient-to-br from-indigo-50 to-violet-50 rounded-xl border border-indigo-100 p-8 text-center">
      <font-awesome-icon icon="fa-solid fa-wand-magic-sparkles" class="text-3xl text-indigo-500 mb-4" />
      <h2 class="text-xl font-semibold text-gray-900 mb-2">{{ t('landing.aiAssistTitle') }}</h2>
      <p class="text-sm text-gray-500 max-w-xl mx-auto leading-relaxed">
        {{ t('landing.aiAssistDesc') }}
      </p>
      <router-link
        to="/settings"
        class="inline-flex items-center mt-4 text-sm text-indigo-600 hover:text-indigo-800 font-medium transition-colors"
      >
        <font-awesome-icon icon="fa-solid fa-gear" class="mr-1.5" />
        {{ t('landing.aiSettings') }}
      </router-link>
    </section>
  </div>
</template><script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>