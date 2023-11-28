/*
 =========================================================
 * Vue Black Dashboard - v1.1.2
 =========================================================

 * Product Page: https://www.creative-tim.com/product/black-dashboard
 * Copyright 2023 Creative Tim (http://www.creative-tim.com)

 =========================================================

 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

 */
import Vue from "vue";
import VueRouter from "vue-router";
import RouterPrefetch from 'vue-router-prefetch'
import App from "./App";
import "bootstrap/dist/css/bootstrap.css";
// TIP: change to import router from "./router/starterRouter"; to start with a clean layout
import router from "./router/index";

import BlackDashboard from "./plugins/blackDashboard";
import i18n from "./i18n"
import './registerServiceWorker'
import store from "./store";
Vue.use(BlackDashboard);
Vue.use(VueRouter);
Vue.use(RouterPrefetch);

/* eslint-disable no-new */
new Vue({
  router,
  store,
  i18n,
  render: h => h(App),
  created() {
    this.$store.dispatch('changeSelectedTicker', { name: 'AAPL' });
    this.$store.dispatch('changeSelectedStockSymbol', 'AAPL');
  },
}).$mount("#app");