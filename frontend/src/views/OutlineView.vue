<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 mb-6">
      <font-awesome-icon icon="fa-solid fa-list" class="text-amber-600 mr-2" />
      {{ t('outline.title') }}
    </h1>

    <ErrorBanner v-if="outlineStore.error" :message="outlineStore.error" />

    <OutlineForm ref="formRef" :novel-id="novelId" />
    <OutlineList :novel-id="novelId" @edit-outline="onEditOutline" />
  </div>
</template><script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useOutlineStore } from '../stores/outline'
import ErrorBanner from '../components/ErrorBanner.vue'
import OutlineForm from '../components/OutlineForm.vue'
import OutlineList from '../components/OutlineList.vue'

const props = defineProps({
  novelId: { type: String, required: true }
})

const { t } = useI18n()

const outlineStore = useOutlineStore()
const formRef = ref<any>(null)

const novelId = computed(() => Number.parseInt(props.novelId))

onMounted(() => {
  outlineStore.fetchAll({ novelId: novelId.value })
})

function onEditOutline(ol) {
  formRef.value?.startEdit(ol)
}
</script>