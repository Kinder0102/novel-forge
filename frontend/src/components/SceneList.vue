<template>
  <div>
    <div v-if="store.loading && !store.scenes.length" class="flex justify-center py-4">
      <font-awesome-icon icon="fa-solid fa-spinner" spin class="text-rose-600 text-xl" />
    </div>

    <div v-else-if="!store.scenes.length" class="text-center py-8 text-gray-400">
      <font-awesome-icon icon="fa-solid fa-clapperboard" class="text-3xl mb-2" />
      <p>{{ t('scene.noScenes') }}</p>
      <p class="text-sm mt-1">{{ t('scene.noScenesDesc') }}</p>
    </div>

    <div v-else class="space-y-3">
      <div
        v-for="scene in store.scenes"
        :key="scene.id"
        class="bg-white rounded-xl shadow-sm border border-gray-200 p-5"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1 min-w-0">
            <div class="flex items-center space-x-2 mb-1">
              <span class="w-6 h-6 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center text-xs font-bold shrink-0">
                {{ scene.scene_number }}
              </span>
              <h4 class="font-semibold text-gray-900 truncate">{{ scene.title }}</h4>
            </div>
            <p class="text-sm text-gray-500">{{ scene.description }}</p>
          </div>

          <div class="flex space-x-1 ml-2 shrink-0">
            <button
              @click="editScene(scene)"
              class="p-1.5 rounded-lg text-gray-400 hover:text-rose-600 hover:bg-rose-50 transition-colors text-xs"
              :title="t('common.edit')"
            >
              <font-awesome-icon icon="fa-solid fa-pen-to-square" />
            </button>
            <button
              @click="confirmDelete(scene.id)"
              class="p-1.5 rounded-lg text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors text-xs"
              :title="t('common.delete')"
            >
              <font-awesome-icon icon="fa-solid fa-trash" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <ConfirmModal
      :visible="showConfirm"
      :title="t('common.confirm')"
      :message="t('scene.deleteConfirm')"
      @confirm="performDelete"
      @cancel="cancelDelete"
    />
  </div>
</template><script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useSceneStore } from '../stores/scene'
import ConfirmModal from './ConfirmModal.vue'

const props = defineProps({
  chapterTitleId: { type: Number, required: true }
})

const emit = defineEmits<{ 'edit-scene': [scene: any] }>()

const { t } = useI18n()
const store = useSceneStore()
const deletingId = ref<number | null>(null)
const showConfirm = ref(false)

function confirmDelete(id) {
  deletingId.value = id
  showConfirm.value = true
}

function cancelDelete() {
  deletingId.value = null
  showConfirm.value = false
}

async function performDelete() {
  if (deletingId.value) {
    await store.remove(deletingId.value)
  }
  cancelDelete()
}

function editScene(scene) {
  emit('edit-scene', scene)
}
</script>