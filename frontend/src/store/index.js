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
    selectedStockSymbol: '',
    stockDataCache: {} // Cache for stock data
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
    },
    getStockData: (state) => (symbol) => {
      return state.stockDataCache[symbol];
    }
  },
  mutations: {
    mutateSelectedTicker(state, payload) {
      state.selectedTicker.name = payload.name;
      state.selectedTicker.info = payload.info;
    },
    setSelectedStockSymbol(state, symbol) { 
      state.selectedStockSymbol = symbol;
    },
    setStockDataCache(state, { symbol, data }) {
      Vue.set(state.stockDataCache, symbol, data); // Ensures reactivity
    }
  },
  actions: {
    async fetchStockData({ commit }, symbol) {
        commit('setLoading', true); // Assuming you have a mutation to set loading state
        try {
          const response = await axios.get(`http://127.0.0.1:5000/stock/${symbol}/prices`);
          commit('setStockDataCache', { symbol, data: response.data });
          commit('setSelectedStockSymbol', symbol); // Update the selected stock symbol
          commit('setLoading', false);
        } catch (error) {
          console.error('Error fetching stock data:', error);
          commit('setLoading', false);
        }
    },
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
