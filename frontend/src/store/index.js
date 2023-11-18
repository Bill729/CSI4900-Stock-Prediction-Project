import Vue from "vue";
import Vuex from "vuex";
import axios from 'axios';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    selectedTicker: {
      name: "",
      info: []
    },
    selectedStockSymbol: '' 
  },
  getters: {
    getSelectedTickerData: (state) => () => {
      return {
        name: state.selectedTicker.name,
        info: state.selectedTicker.info
      }
    },
    getSelectedStockSymbol: (state) => {
      return state.selectedStockSymbol; 
    }
  },
  mutations: {
    mutateSelectedTicker(state, payload) {
      state.selectedTicker.name = payload.name;
      state.selectedTicker.info = payload.info;
    },
    setSelectedStockSymbol(state, symbol) { 
      state.selectedStockSymbol = symbol;
    }
  },
  actions: {
    async changeSelectedTicker(context, payload) {
      const uri = 'http://127.0.0.1:5000/stock/' + payload.name + '/info';
      const res = await axios.get(uri);
      context.commit("mutateSelectedTicker", { name: payload.name, info: res.data });
      return res;
    },
    changeSelectedStockSymbol(context, symbol) { 
      context.commit('setSelectedStockSymbol', symbol);
    }
  }
});
