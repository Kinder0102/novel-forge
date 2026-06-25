<template>
  <div class="max-w-4xl mx-auto space-y-12 py-4">
    <!-- Hero -->
    <section class="text-center space-y-4">
      <h1 class="text-4xl font-extrabold text-gray-900 tracking-tight">NovelForge</h1>
      <p class="text-lg text-gray-500 max-w-2xl mx-auto leading-relaxed">
        一站式小說創作輔助工具，從世界觀架構、角色設計、大綱規劃到場景與章節撰寫，
        搭配 AI 輔助生成，幫你將靈感淬鍊成完整故事。
      </p>
      <router-link
        to="/worldbuilding"
        class="inline-flex items-center px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium shadow-sm"
      >
        <font-awesome-icon icon="fa-solid fa-play" class="mr-2" />
        開始創作
      </router-link>
    </section>

    <!-- Feature Cards -->
    <section>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <router-link
          to="/worldbuilding"
          class="group bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-indigo-200 transition-all duration-200"
        >
          <div class="w-10 h-10 rounded-lg bg-indigo-50 flex items-center justify-center mb-4 group-hover:bg-indigo-100 transition-colors">
            <font-awesome-icon icon="fa-solid fa-globe" class="text-xl text-indigo-500" />
          </div>
          <h2 class="text-lg font-semibold text-gray-900 mb-2">世界觀架構</h2>
          <p class="text-sm text-gray-500 leading-relaxed">
            定義故事的世界觀：類型、時代背景、地理設定與世界法則。AI 可根據主題概念自動生成完整世界觀。
          </p>
        </router-link>

        <router-link
          to="/character"
          class="group bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-emerald-200 transition-all duration-200"
        >
          <div class="w-10 h-10 rounded-lg bg-emerald-50 flex items-center justify-center mb-4 group-hover:bg-emerald-100 transition-colors">
            <font-awesome-icon icon="fa-solid fa-user" class="text-xl text-emerald-500" />
          </div>
          <h2 class="text-lg font-semibold text-gray-900 mb-2">角色設計</h2>
          <p class="text-sm text-gray-500 leading-relaxed">
            創造立體角色：名稱、定位、性格、背景故事與外貌。AI 可根據世界觀自動生成深具魅力的角色。
          </p>
        </router-link>

        <router-link
          to="/outline"
          class="group bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-amber-200 transition-all duration-200"
        >
          <div class="w-10 h-10 rounded-lg bg-amber-50 flex items-center justify-center mb-4 group-hover:bg-amber-100 transition-colors">
            <font-awesome-icon icon="fa-solid fa-list-ol" class="text-xl text-amber-500" />
          </div>
          <h2 class="text-lg font-semibold text-gray-900 mb-2">大綱規劃</h2>
          <p class="text-sm text-gray-500 leading-relaxed">
            規劃故事結構：設定故事標題與摘要，拆分章節。AI 可根據背景資訊自動生成章節大綱。
          </p>
        </router-link>

        <router-link
          to="/scene/0"
          class="group bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-rose-200 transition-all duration-200"
        >
          <div class="w-10 h-10 rounded-lg bg-rose-50 flex items-center justify-center mb-4 group-hover:bg-rose-100 transition-colors">
            <font-awesome-icon icon="fa-solid fa-clapperboard" class="text-xl text-rose-500" />
          </div>
          <h2 class="text-lg font-semibold text-gray-900 mb-2">場景管理</h2>
          <p class="text-sm text-gray-500 leading-relaxed">
            拆解章節為具體場景，規劃每個場景的標題與摘要。AI 可自動拆分章節並生成完整場景內容。
          </p>
        </router-link>

        <router-link
          to="/chapter/0"
          class="group bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-violet-200 transition-all duration-200"
        >
          <div class="w-10 h-10 rounded-lg bg-violet-50 flex items-center justify-center mb-4 group-hover:bg-violet-100 transition-colors">
            <font-awesome-icon icon="fa-solid fa-book-open" class="text-xl text-violet-500" />
          </div>
          <h2 class="text-lg font-semibold text-gray-900 mb-2">章節撰寫</h2>
          <p class="text-sm text-gray-500 leading-relaxed">
            撰寫完整章節內容，管理每章的狀態。AI 可根據大綱自動生成約 2000-4000 字的章節正文。
          </p>
        </router-link>
      </div>
    </section>

    <!-- Workflow -->
    <section class="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
      <h2 class="text-xl font-semibold text-gray-900 text-center mb-8">創作流程</h2>
      <div class="grid grid-cols-1 sm:grid-cols-5 gap-4">
        <div class="text-center">
          <div class="w-10 h-10 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center mx-auto mb-3 font-bold text-sm">1</div>
          <p class="text-sm font-medium text-gray-900">建立世界觀</p>
          <p class="text-xs text-gray-500 mt-1">定義故事基礎</p>
        </div>
        <div class="text-center">
          <div class="w-10 h-10 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto mb-3 font-bold text-sm">2</div>
          <p class="text-sm font-medium text-gray-900">設計角色</p>
          <p class="text-xs text-gray-500 mt-1">賦予角色靈魂</p>
        </div>
        <div class="text-center">
          <div class="w-10 h-10 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center mx-auto mb-3 font-bold text-sm">3</div>
          <p class="text-sm font-medium text-gray-900">規劃大綱</p>
          <p class="text-xs text-gray-500 mt-1">搭建故事骨架</p>
        </div>
        <div class="text-center">
          <div class="w-10 h-10 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center mx-auto mb-3 font-bold text-sm">4</div>
          <p class="text-sm font-medium text-gray-900">拆分場景</p>
          <p class="text-xs text-gray-500 mt-1">細化每個環節</p>
        </div>
        <div class="text-center">
          <div class="w-10 h-10 rounded-full bg-violet-100 text-violet-600 flex items-center justify-center mx-auto mb-3 font-bold text-sm">5</div>
          <p class="text-sm font-medium text-gray-900">撰寫章節</p>
          <p class="text-xs text-gray-500 mt-1">完成故事成文</p>
        </div>
      </div>
    </section>

    <!-- AI Features Highlight -->
    <section class="bg-gradient-to-br from-indigo-50 to-violet-50 rounded-xl border border-indigo-100 p-8 text-center">
      <font-awesome-icon icon="fa-solid fa-wand-magic-sparkles" class="text-3xl text-indigo-500 mb-4" />
      <h2 class="text-xl font-semibold text-gray-900 mb-2">AI 輔助創作</h2>
      <p class="text-sm text-gray-500 max-w-xl mx-auto leading-relaxed">
        每個模組皆內建 AI 生成功能，可自訂 API 金鑰與模型。
        從世界觀架構、角色設計到大綱與章節撰寫，AI 全程為你的創作加速。
      </p>
      <router-link
        to="/settings"
        class="inline-flex items-center mt-4 text-sm text-indigo-600 hover:text-indigo-800 font-medium transition-colors"
      >
        <font-awesome-icon icon="fa-solid fa-gear" class="mr-1.5" />
        AI 設定
      </router-link>
    </section>
  </div>
</template>
