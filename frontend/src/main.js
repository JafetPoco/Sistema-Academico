import { createApp } from 'vue'
import axios from 'axios'
// Bootstrap CSS & JS (bundle includes Popper)
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css'


import App from './App.vue'
import router from './router'

// Configure axios defaults so all components send cookies and use API base
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000'
axios.defaults.baseURL = API_BASE
axios.defaults.withCredentials = true

const app = createApp(App)
app.use(router)
app.mount('#app')
