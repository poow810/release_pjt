import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import piniaPluginPersist from 'pinia-plugin-persist'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
// import vuetify from './plugins/vuetify'
import './assets/styles/global.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

// Global style 적용
const customStyles = document.createElement('style');
customStyles.innerHTML = `
  body {
    font-family: 'GmarketSans', sans-serif;
  }
`;
document.head.appendChild(customStyles);

// 유투브
import YouTube from 'vue3-youtube'

const app = createApp(App)
const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)
pinia.use(piniaPluginPersist)
// app.use(vuetify)
app.use(pinia)
app.use(router)

app.component('Youtube', YouTube)
app.mount('#app')