<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">
        <font-awesome-icon icon="fa-solid fa-globe" class="text-indigo-600 mr-2" />
        {{ t('worldbuilding.title') }}
      </h1>
    </div>

    <ErrorBanner v-if="store.error" :message="store.error" />

    <WorldbuildingForm ref="formRef" :novel-id="novelId" />
    <WorldbuildingList @edit-worldbuilding="handleEditWorld" />
  </div>
</template><script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useWorldbuildingStore } from '../stores/worldbuilding'
import WorldbuildingForm from '../components/WorldbuildingForm.vue'
import WorldbuildingList from '../components/WorldbuildingList.vue'
import ErrorBanner from '../components/ErrorBanner.vue'

const props = defineProps<{
  novelId: string
}>()

const { t } = useI18n()

const store = useWorldbuildingStore()
const formRef = ref<InstanceType<typeof WorldbuildingForm> | null>(null)

const novelId = computed(() => Number.parseInt(props.novelId))

function handleEditWorld(wb: Record<string, unknown>) {
  formRef.value?.startEdit(wb)
}

onMounted(() => {
  store.fetchAll(novelId.value)
})
</script>