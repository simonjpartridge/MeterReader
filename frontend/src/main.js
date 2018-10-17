import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'

Vue.config.productionTip = false


// axios.defaults.baseURL = 'http://192.168.1.238:5005'




new Vue({
  render: h => h(App)
}).$mount('#app')
