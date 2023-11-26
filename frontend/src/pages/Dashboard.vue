<template>
  <div>
    <div v-if="loading" class="overlay">
      <div class="loader"></div>
    </div>
    <!-- <div v-else> -->
    <div class="chart-container" v-if="selectedStock">
      <div class="chart-controls">
        <button @click="updateTimeFrame('1W')">1W</button>
        <button @click="updateTimeFrame('1M')">1M</button>
        <button @click="updateTimeFrame('3M')">3M</button>
        <button @click="updateTimeFrame('1Y')">1Y</button>
        <button @click="updateTimeFrame('ALL')">ALL</button>
      </div>
      <div class="lineChart">
        <canvas id="myChart"></canvas>
      </div>
    </div>
    <!-- {{ this.$store.getters.getSelectedTickerData() }}
    {{ Object.keys(this.$store.getters.getSelectedTickerData().info).length }} -->
    <div style="min-width: auto; min-height: auto; display: grid; grid-gap: 1em; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));">
      <!-- v-if="($store.getters.getSelectedTickerData().info)[key] != 'N/A'" -->
      <card style="width: auto;" v-for="key in Object.keys(this.$store.getters.getSelectedTickerData().info)" type="chart">
        <h5 class="card-category">{{ key }}</h5>
        <h3 class="card-title">
          <!-- <i class="tim-icons icon-bell-55 text-primary "></i> -->
          {{ ($store.getters.getSelectedTickerData().info)[key] }}
        </h3>
      </card>
    </div>
    <!-- Remaining content of the Dashboard -->
    <div class="row">
      <!-- Other content rows and cards -->
    </div>
    <!-- ... other rows and components ... -->
  <!-- </div> -->
  </div>
</template>

<script>
import Chart from 'chart.js';
import axios from 'axios';
import moment from 'moment';

export default {
  name: 'Dashboard',
  data(){
    return{
      loading: false,
      numberOfColumns: 3,
      allData: null,
      chart: null,
    }
  },
  mounted() {
    if (this.selectedStock) {
      this.fetchAndDisplayStockData(this.selectedStock);
    }
  },
  computed: {
    selectedStock() {
      return this.$store.getters.getSelectedStockSymbol;
    }
  },
  watch: {
    selectedStock(newSymbol, oldSymbol) {
      if (newSymbol && newSymbol !== oldSymbol) {
        this.loading = true; // Start loading as soon as a new stock is selected
        this.fetchAndDisplayStockData(newSymbol);
      }
    },
    allData(newData, oldData) {
      if (newData !== oldData) {
        this.createChart(newData, 'ALL');
      }
    }
  },
  // computed: {
  //   gridStyle() {
  //     return {
  //       gridTemplateColumns: `repeat(${this.numberOfColumns}, minmax(100px, 1fr))`
  //     }
  //   }
  // },
  methods: {
    async fetchAndDisplayStockData(stockSymbol) {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/stock/${stockSymbol}/prices`);
     // console.log('Fetched data:', response.data); // Log the fetched data
      this.allData = response.data;
      this.createChart(this.allData, 'ALL');
    } catch (error) {
      console.error('Error fetching data:', error);
    }finally {
        this.loading = false; // Stop loading
      }
    },
    createChart(stockData, timeFrame) {
      const filteredData = this.filterData(stockData, timeFrame);
      const ctx = document.getElementById('myChart').getContext('2d');
      const labels = Object.keys(filteredData.historical).map(timestamp =>
        moment.unix(timestamp).format('MMM YYYY')
      );
      const data = Object.values(filteredData.historical);

      if (this.chart) {
        this.chart.destroy();
      }
      // console.log("Predicted",filteredData.predicted);
      // console.log("Historical", filteredData.historical);
      // console.log(labels);
      // console.log(data);
      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: this.selectedStock,
            data,
            fill: false,
            borderColor: '#007bff',
            tension: 0.1
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: false,
            },
          },
          plugins: {
            legend: {
              display: true,
            },
            tooltip: {
              mode: 'index',
              intersect: false,
            },
          },
        },
      });
    },
    filterData(stockData, timeFrame) {
      if (!stockData || !stockData.historical) {
      console.error('Invalid or missing stock data');
      return {};
    }
        if (timeFrame === 'ALL') {
          return stockData; 
        }
  
        const endDate = moment().unix();
        let startDate;
  
        switch (timeFrame) {
          case '1W':
            startDate = moment().subtract(1, 'weeks').unix();
            break;
          case '1M':
            startDate = moment().subtract(1, 'months').unix();
            break;
          case '3M':
            startDate = moment().subtract(3, 'months').unix();
            break;
          case '1Y':
            startDate = moment().subtract(1, 'years').unix();
            break;
          default:
            startDate = moment().subtract(1, 'years').unix();
        }
  
        return {
          historical: Object.fromEntries(
            Object.entries(stockData.historical).filter(
              ([timestamp]) => timestamp >= startDate && timestamp <= endDate
            )
          ),
        };
    },
    updateTimeFrame(timeFrame) {
      this.createChart(this.allData, timeFrame);
    },
    async getTicker() {
      this.$store.getters.getSelectedTickerData();
    },
  }, 
};
</script>

<style scoped>

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loader {
  border: 5px solid #f3f3f3;
  border-top: 5px solid #3498db;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.chart-container {
  text-align: left;
  padding-left: 20px;
  margin-left: 20px;
}

.lineChart {
  width: 100%;
  max-width: 600px;
  height: 300px;
  margin-left: 0;
  margin-right: auto;
  position: relative; 
}

.chart-controls {
  text-align: left; 
  margin-bottom: 10px; 
  margin-left: 170px;
}

.chart-controls button {
  margin: 5px;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.chart-controls button:hover {
  background-color: #0056b3;
}
</style>
