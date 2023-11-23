<template>
  <div>
    <div v-if="loading" class="loading">Loading...</div>
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
      numberOfColumns: 3
    }
  },
  computed: {
    selectedStock() {
      return this.$store.getters.getSelectedStockSymbol;
    }
  },
  watch: {
    selectedStock(newSymbol, oldSymbol) {
      if (newSymbol !== oldSymbol && newSymbol !== '') {
        this.fetchAndDisplayStockData(newSymbol);
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
      this.loading = true;
    try {
      const response = await axios.get(`http://127.0.0.1:5000/stock/${stockSymbol}/prices`);
      this.allData = response.data;
      this.createChart(this.allData, 'ALL');
    } catch (error) {
      console.error('Error fetching data:', error);
    }finally {
        this.loading = false;
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
    }
  }, 
};
</script>

<style scoped>
.chart-container {
  text-align: center;
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

.lineChart {
  width: 100%;
  max-width: 600px;
  height: 300px;
  margin: auto;
}
.loading {
  /* Styling for your loading indicator */
  text-align: center;
  padding: 20px;
}
/* Other styles... */
</style>
