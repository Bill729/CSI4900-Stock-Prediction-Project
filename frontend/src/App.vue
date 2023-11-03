<template>
  <div>
    <notifications></notifications>
    <router-view :key="$route.fullPath"></router-view>
</div>
</template>

<script>

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
    }
<<<<<<< HEAD
  }
=======
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
>>>>>>> a82031126731b5c9337f4bd32a4339ffeb880227
</script>

<style lang="scss"></style>
