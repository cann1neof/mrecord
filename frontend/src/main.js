import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import store from './store'
import YmapPlugin from 'vue-yandex-maps'
import VuePhoneNumberInput from 'vue-phone-number-input';
import 'vue-phone-number-input/dist/vue-phone-number-input.css';

Vue.component('vue-phone-number-input', VuePhoneNumberInput);

const settings = {
  apiKey: '0743cdc0-0634-4b6f-be02-c546c5add538',
  lang: 'ru_RU',
  coordorder: 'latlong',
  version: '2.1'
}
Vue.use(YmapPlugin, settings)

Vue.config.productionTip = false

new Vue({
  vuetify,
  router,
  store,
  render: h => h(App)
}).$mount('#app')
