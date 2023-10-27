<template>
  <div>
    <notifications></notifications>
    <router-view :key="$route.fullPath"></router-view>
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";

import LineChart from "./components/LineChart";

  export default {
    methods: {
      disableRTL() {
        if (!this.$rtl.isRTL) {
          this.$rtl.disableRTL();
        }
      },
      toggleNavOpen() {
        let root = document.getElementsByTagName('html')[0];
        root.classList.toggle('nav-open');
      }
    },
    mounted() {
      this.$watch('$route', this.disableRTL, { immediate: true });
      this.$watch('$sidebar.showSidebar', this.toggleNavOpen)
    },
    components: {
      LineChart
    },
    data(){
      return{
        arrStock: [],
        arrCurrentPrice: [],
        stockData: {
          "AAPL": {
          "currentPrice": 166.89
        },
        "AMZN": {
          "currentPrice": 119.57
        },
        "BRK-B": {
          "currentPrice": 336.16
        },
        "GOOGL": {
          "currentPrice": 122.28
        },
        "JNJ": {
          "currentPrice": 149.0
        },
        "META": {
          "currentPrice": 288.35
        },
        "MSFT": {
          "currentPrice": 327.89
        },
        "PG": {
          "currentPrice": 149.8
        },
        "V": {
          "currentPrice": 231.28
        },
        "WMT": {
          "currentPrice": 161.77
        }
      }
    }
  },
    async created(){
      try{
        const { data } = await axios.get('http://127.0.0.1:5000/tickers');
        console.log('data', data);
        const { data1 } = await axios.get('http://127.0.0.1:5000/stock/AAPL/info');
        console.log('data1', data1);
        
        for(const stockSymbol1 in this.stockData){
        const stock = this.stockData[stockSymbol1];

        const currentPrice = stock.currentPrice;
        const stockSymbol = stockSymbol1;
        

        console.log(stockSymbol, currentPrice);
        
      }
       

      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }
  };
</script>

<style lang="scss"></style>
