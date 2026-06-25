import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faFeather,
  faHome,
  faGlobe,
  faUsers,
  faList,
  faListOl,
  faClapperboard,
  faBook,
  faPlus,
  faEdit,
  faTrash,
  faChevronDown,
  faChevronUp,
  faSpinner,
  faDownload,
  faMagicWandSparkles,
  faArrowRight,
  faBars,
  faTimes,
  faSave,
  faGear,
  faShieldHalved,
  faEye,
  faEyeSlash,
  faUndo,
  faCheck,
  faExclamationTriangle,
  faPlay,
  faUser,
  faBookOpen
} from '@fortawesome/free-solid-svg-icons'
import router from './router'
import App from './App.vue'
import './style.css'

library.add(
  faFeather,
  faHome,
  faGlobe,
  faUsers,
  faList,
  faListOl,
  faClapperboard,
  faBook,
  faPlus,
  faEdit,
  faTrash,
  faChevronDown,
  faChevronUp,
  faSpinner,
  faDownload,
  faMagicWandSparkles,
  faArrowRight,
  faBars,
  faTimes,
  faSave,
  faGear,
  faShieldHalved,
  faEye,
  faEyeSlash,
  faUndo,
  faCheck,
  faExclamationTriangle,
  faPlay,
  faUser,
  faBookOpen
)

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')
