import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import './icons'
import router from './router'
import App from './App.vue'
import i18n from './i18n'
import './style.css'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(i18n)
app.component('font-awesome-icon', FontAwesomeIcon)

const el = document.getElementById('app')
if (el) {
  app.mount(el)
} else {
  console.error('[NovelForge] Mount point #app not found, unable to start application')
}

