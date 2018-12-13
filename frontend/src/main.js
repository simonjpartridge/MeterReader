import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'

Vue.config.productionTip = false


axios.defaults.baseURL = 'http://localhost:80'



new Vue({
  render: h => h(App)
}).$mount('#app')

Vue.config.devtools = true
