<template>
  <div>
    <div v-if="store.loading && !store.outlines.length" class="flex justify-center py-8">
      <font-awesome-icon icon="fa-solid fa-spinner" spin class="text-amber-600 text-2xl" />
    </div>

    <div v-else-if="!store.outlines.length" class="text-center py-8 text-gray-400">
      <font-awesome-icon icon="fa-solid fa-list" class="text-4xl mb-3" />
      <p>{{ t('outline.noOutlines') }}</p>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="ol in store.outlines"
        :key="ol.id"
        class="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-gray-900">{{ ol.title }}</h3>
            <p class="text-gray-500 text-sm mt-1">{{ ol.description }}</p>
          </div>
          <div class="flex space-x-1 ml-2">
            <button
              @click="editOutline(ol)"
              class="p-1.5 rounded-lg text-gray-400 hover:text-amber-600 hover:bg-amber-50 transition-colors"
            >
              <font-awesome-icon icon="fa-solid fa-edit" class="text-sm" />
            </button>
            <button
              @click="confirmDelete(ol.id)"
              class="p-1.5 rounded-lg text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors"
            >
              <font-awesome-icon icon="fa-solid fa-trash" class="text-sm" />
            </button>
          </div>
        </div>

        <div class="flex gap-2 mt-4 pt-3 border-t border-gray-100">
          <router-link
            :to="`/novel/${novelId}/scene/${ol.id}`"
            class="inline-flex items-center text-sm bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg px-3 py-1.5 transition-colors"
          >
            <font-awesome-icon icon="fa-solid fa-clapperboard" class="mr-1" />
            {{ t('outline.planScenes') }}
          </router-link>
          <router-link
            :to="`/novel/${novelId}/chapter/${ol.id}`"
            class="inline-flex items-center text-sm bg-amber-100 hover:bg-amber-200 text-amber-700 rounded-lg px-3 py-1.5 transition-colors"
          >
            <font-awesome-icon icon="fa-solid fa-book" class="mr-1" />
            {{ t('outline.generateChapters') }}
          </router-link>
        </div>
      </div>
    </div>

    <ConfirmModal
      :visible="showConfirm"
      :title="t('common.confirm')"
      :message="t('outline.deleteConfirm')"
      @confirm="performDelete"
      @cancel="cancelDelete"
    />
  </div>
</template><script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useOutlineStore } from '../stores/outline'
import ConfirmModal from './ConfirmModal.vue'

const props = defineProps({
  novelId: { type: Number, required: true }
})

const emit = defineEmits<{ 'edit-outline': [ol: any] }>()

const { t } = useI18n()
const store = useOutlineStore()
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

function editOutline(ol) {
  emit('edit-outline', ol)
}
</script>