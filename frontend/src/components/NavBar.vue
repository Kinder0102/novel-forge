<template>
  <nav class="bg-gray-900 text-white shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <router-link to="/" class="flex items-center space-x-2 text-xl font-bold hover:text-indigo-300 transition-colors">
          <font-awesome-icon icon="fa-solid fa-feather" class="text-indigo-400" />
          <span>NovelForge</span>
        </router-link>

        <!-- Desktop nav -->
        <div class="hidden md:flex space-x-1">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="flex items-center space-x-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors"
            :class="$route.path === item.path ? 'bg-gray-800 text-indigo-300' : 'text-gray-300 hover:bg-gray-800 hover:text-white'"
          >
            <font-awesome-icon :icon="item.icon" class="text-xs" />
            <span>{{ item.label }}</span>
          </router-link>
        </div>

        <!-- Mobile menu button -->
        <button @click="mobileOpen = !mobileOpen" class="md:hidden p-2 rounded-lg hover:bg-gray-800 transition-colors">
          <font-awesome-icon :icon="mobileOpen ? 'fa-solid fa-times' : 'fa-solid fa-bars'" />
        </button>
      </div>
    </div>

    <!-- Mobile nav -->
    <div v-if="mobileOpen" class="md:hidden border-t border-gray-800">
      <div class="px-2 pt-2 pb-3 space-y-1">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          @click="mobileOpen = false"
          class="flex items-center space-x-2 px-3 py-2 rounded-lg text-base font-medium transition-colors"
          :class="$route.path === item.path ? 'bg-gray-800 text-indigo-300' : 'text-gray-300 hover:bg-gray-800 hover:text-white'"
        >
          <font-awesome-icon :icon="item.icon" class="text-sm w-4" />
          <span>{{ item.label }}</span>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

const mobileOpen = ref(false)

const navItems = [
  { path: '/', label: '首頁', icon: 'fa-solid fa-home' },
  { path: '/worldbuilding', label: '世界觀', icon: 'fa-solid fa-globe' },
  { path: '/character', label: '角色', icon: 'fa-solid fa-users' },
  { path: '/outline', label: '大綱', icon: 'fa-solid fa-list' },
  { path: '/scene/0', label: '場景', icon: 'fa-solid fa-clapperboard' },
  { path: '/chapter/0', label: '章節', icon: 'fa-solid fa-book' },
  { path: '/settings', label: '設定', icon: 'fa-solid fa-gear' }
]
</script>
