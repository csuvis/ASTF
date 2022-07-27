/*
 * @Description: 
 * @Version: 2.0
 * @Autor: 葛璐豪
 * @Date: 2020-10-04 22:21:39
 * @LastEditors: Seven
 * @LastEditTime: 2021-01-15 21:19:42
 */
import App from './App.vue'
import Vue from 'vue'
import store from './store'
import ElementUI from 'element-ui'

import 'normalize.css/normalize.css'
import 'nprogress/nprogress.css'
import 'assets/style/styles.scss'

Vue.prototype.$viewSW = viewSW
Vue.prototype.$viewPx = viewPx
Vue.use(ElementUI)

Vue.config.productionTip = false

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
