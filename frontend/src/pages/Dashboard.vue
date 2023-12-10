<template>
  <div>
    <div id="top-wrapper">
      <div class="chart-container" v-if="selectedStock">
        <div id="basic-info" v-if="this.$store.getters.getSelectedTickerData().name">
          <h1>${{ this.$store.getters.getSelectedTickerData().info.currentPrice }}</h1>
          <h2>{{ this.$store.getters.getSelectedTickerData().info.companyName }}</h2>
        </div>
        <div class="line-chart-container">
        <div class="chart-controls">
          <button :class="['chart-control-button', '1W' === activeTimeFrame ? 'active' : '']" @click="updateTimeFrame('1W')">1W
            <span v-if="performanceData['1w']" :class="{'positive': performanceData['1w'] >= 0, 'negative': performanceData['1w'] < 0}">{{ performanceData['1w'] | formatPercentage }}</span>
          </button>
          <button :class="['chart-control-button', '1M' === activeTimeFrame ? 'active' : '']" @click="updateTimeFrame('1M')">1M
            <span v-if="performanceData['1m']" :class="{'positive': performanceData['1m'] >= 0, 'negative': performanceData['1m'] < 0}">{{ performanceData['1m'] | formatPercentage }}</span>
          </button>
          <button :class="['chart-control-button', '3M' === activeTimeFrame ? 'active' : '']" @click="updateTimeFrame('3M')">3M
            <span v-if="performanceData['3m']" :class="{'positive': performanceData['3m'] >= 0, 'negative': performanceData['3m'] < 0}">{{ performanceData['3m'] | formatPercentage }}</span>
          </button>
          <button :class="['chart-control-button', '1Y' === activeTimeFrame ? 'active' : '']" @click="updateTimeFrame('1Y')">1Y
            <span v-if="performanceData['1y']" :class="{'positive': performanceData['1y'] >= 0, 'negative': performanceData['1y'] < 0}">{{ performanceData['1y'] | formatPercentage }}</span>
          </button>
          <button :class="['chart-control-button', 'ALL' === activeTimeFrame ? 'active' : '']" @click="updateTimeFrame('ALL')">ALL
            <span v-if="performanceData['all']" :class="{'positive': performanceData['all'] >= 0, 'negative': performanceData['all'] < 0}">{{ performanceData['all'] | formatPercentage }}</span>
          </button>
          <button :class="['chart-control-button', 'chart-control-button-7d-pred', '7D_PRED' === activeTimeFrame ? 'active' : '']" @click="updateTimeFrame('7D_PRED')">7D Predicted
            <span v-if="performanceData['1w_predicted']" :class="{'positive': performanceData['1w_predicted'] >= 0, 'negative': performanceData['1w_predicted'] < 0}">
              {{ performanceData['1w_predicted'] | formatPercentage }}</span>
          </button>
        </div>
        <div class="lineChart">
          <canvas id="myChart"></canvas>
          <div v-if="loading" class="overlay">
            <div class="loader"></div>
          </div>
        </div>
      </div>
      </div>
      <div id="cards">
      <!-- v-if="($store.getters.getSelectedTickerData().info)[key] != 'N/A'" -->
      <card style="width: auto;" v-if="checkDesiredKey(key)" v-for="key in Object.keys(this.$store.getters.getSelectedTickerData().info)" type="chart">
        <h5>{{ displayCardNames[key] }}</h5>
        <h3 v-if="typeof(($store.getters.getSelectedTickerData().info)[key]) === 'number' && formatDecimalNumber($store.getters.getSelectedTickerData().info[key], 2) != false">
          <!-- <i class="tim-icons icon-bell-55 text-primary "></i> -->
          {{ formatDecimalNumber($store.getters.getSelectedTickerData().info[key], 2) }}
        </h3>
        <h3 v-else>
          <!-- <i class="tim-icons icon-bell-55 text-primary "></i> -->
          {{ ($store.getters.getSelectedTickerData().info)[key] }}
        </h3>
      </card>
      </div>
    </div>
    <h2 id="table-title">Model Performance (7D Predicted)</h2>
    <div id="table-div-wrapper">
      <div id="table-div">
        <table class="table table-dark">
          <thead>
            <tr>
              <th scope="col">Date</th>
              <th scope="col">Mean Square Error</th>
              <th scope="col">Mean Absolute Error</th>
              <th scope="col">Root Mean Square Error</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="el in this.modelPerformanceToDays()">
              <td>{{ el[0] }}</td>
              <td>{{ formatDecimalNumber(el[1]['MAE'], 2) }}</td>
              <td>{{ formatDecimalNumber(el[1]['MSE'], 2) }}</td>
              <td>{{ formatDecimalNumber(el[1]['RMSE'], 2) }}</td>
            </tr>
            <tr></tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- {{ this.$store.getters.getSelectedTickerData() }} -->
    <!-- {{ Object.keys(this.$store.getters.getSelectedTickerData().info) }} -->

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
import moment from 'moment';
import axios from 'axios';

export default {
  name: 'Dashboard',
  data(){
    return{
      loading: false,
      allData: null,
      chart: null,
      activeTimeFrame: 'ALL', // Set a default active time frame if needed
      displayCardNames: {},
      predictedModelPerformance: [],
      performanceData: {}
    }
  },
  mounted() {
    if (this.selectedStock) {
      this.fetchAndDisplayStockData(this.selectedStock);
    }

    // copied keys from metrics array in backend /!\
    this.displayCardNames = {
      "marketCap": "Market Cap", 
      "sector": "Sector", 
      "industry": "Industry",
      "dividendYield": "Dividend Yield", 
      "trailingPE": "Trailing PE", 
      "earningsQuarterlyGrowth": "Earnings Quarterly Growth",
      "currentPrice": "Current Price", 
      "regularMarketVolume": "Regular Market Volume", 
      "beta": "Beta",
      "fiftyTwoWeekLow": "Fifty-Two Week Low", 
      "fiftyTwoWeekHigh": "Fifty-Two Week High", 
      "currency": "Currency"
    }

    this.fillPerformanceArr();

    console.log(this.modelPerformanceToDays());
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
        this.activeTimeFrame = 'ALL'; // Reset the active time frame
        this.fetchAndDisplayStockData(newSymbol);
      }
    },
    allData(newData, oldData) {   
      if (newData !== oldData) {
        this.createChart(newData, 'ALL');
      }
    }
  },
  filters: {
    formatPercentage(value) {
      return `${value.toFixed(2)}%`;
    }
  },
  methods: {
    async fillPerformanceArr(){
      const uri = 'http://127.0.0.1:5000/model/performance';
      await axios.get(uri)
      .then((res) => {
        console.log(res);
        this.predictedModelPerformance = res.data;
        return res.data;
      })
      .catch((error) => {
        console.error(error);
      });
    },
    modelPerformanceToDays(){
      let res = []
      for(var el in this.predictedModelPerformance){
        var date = new Date();
        date.setDate(date.getDate() + Number(el) - 1);
        var dateStr = date.toLocaleString('default', { month: 'short', day: 'numeric' });
        res.push([dateStr, this.predictedModelPerformance[el]])
      }
      return res;
    },
    selectStock(stockSymbol) {
      this.$store.dispatch('fetchStockData', stockSymbol);
    },
    checkDesiredKey(key){
      return !['currentPrice', 'companyName'].includes(key)
    },
    formatDecimalNumber(value, precision){
      let splitDecimalValue = value.toString().split('.');
      // console.log(splitDecimalValue)
      if(splitDecimalValue.length == 1) return false;

      let lenOfNonDecimal = splitDecimalValue[0].toString().length
      // console.log(value.toPrecision(lenOfNonDecimal + 2))
      return value.toPrecision(lenOfNonDecimal + precision);
    },
    async fetchAndDisplayStockData(stockSymbol) {
      this.loading = true;
      const cachedData = this.$store.getters.getStockData(stockSymbol);
      if (cachedData) {
        this.allData = cachedData;
        this.createChart(this.allData, this.activeTimeFrame); // Use the active time frame instead of 'ALL'
      } else {
        // If there's no cache, fetch the data
        await this.$store.dispatch('fetchStockData', stockSymbol);
        // After dispatching, the cache will be updated, so you can retrieve it
        this.allData = this.$store.getters.getStockData(stockSymbol);
        // Make sure to handle the case when the API call fails and allData remains undefined
        if (this.allData) {
          //this.performanceData = this.allData.performance;
          this.createChart(this.allData, this.activeTimeFrame);
        }
      }
      this.loading = false;
    },
    createChart(stockData, timeFrame) {
      // Log the data to debug if the timestamps are correct
    console.log('Creating chart with data:', stockData);
    const ctx = document.getElementById('myChart').getContext('2d');

    if (this.chart) {
      this.chart.destroy();
    }

    const filteredData = this.filterData(stockData, timeFrame);

    // Generate labels and data for historical data
    const historicalLabels = Object.keys(filteredData.historical).map(timestamp =>
      moment.unix(timestamp).format('MMM D, YYYY')
    );
    const historicalDataPoints = Object.values(filteredData.historical);

    // Generate labels and data for predicted data
    const predictedLabels = Object.keys(filteredData.predicted).map(timestamp =>
      moment.unix(timestamp).format('MMM D, YYYY')
    );
    const predictedDataPoints = Object.values(filteredData.predicted);
    // let spacedPredictedData = [];
    // let spacedPredictedLabels = [];
    // if (timeFrame === 'ALL' && predictedDataPoints.length > 7) {
    //   // For example, take one data point per interval (e.g., every 3 days)
    //   const interval = Math.ceil(predictedDataPoints.length / 7);
    //   for (let i = 0; i < predictedDataPoints.length; i += interval) {
    //     spacedPredictedData.push(predictedDataPoints[i]);
    //     spacedPredictedLabels.push(predictedLabels[i]);
    //   }
    // } else {
    //   spacedPredictedData = predictedDataPoints;
    //   spacedPredictedLabels = predictedLabels;
    // }
    // Create the chart with the separate datasets
    console.log("Performance", stockData.performance);
    this.chart = new Chart(ctx, {
      type: 'line',
      data: {
        datasets: [
          {
            label: `${this.selectedStock} - Historical`,
            data: historicalDataPoints.map((value, index) => ({ x: historicalLabels[index], y: value })),
            fill: false,
            borderColor: '#007bff',
            tension: 0.1
          },
          {
            label: `${this.selectedStock} - Predicted`,
            data: predictedDataPoints.map((value, index) => ({ x: predictedLabels[index], y: value })),
            fill: false,
            borderColor: '#ff4500',
            pointBackgroundColor: '#ff4500', // Set the point background color to match the border color
            borderWidth: 2,
            borderDash: [5, 5],
            tension: 0.1
          }
        ]
      },
      options: {
        scales: {
          xAxes: [{
            type: 'time',
            time: {
              parser: 'MMM D, YYYY',
              unit: 'day',
              displayFormats: {
                day: 'MMM D, YYYY'
              },
              tooltipFormat: 'll'
            },
            distribution: 'linear'
          }],
          yAxes: [{
            beginAtZero: false
          }]
        },
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true
          },
          tooltip: {
            mode: 'index',
            intersect: false
          }
        },
        maintainAspectRatio: false,
      }
    });
    this.performanceData = this.calculatePerformanceData(stockData.performance, timeFrame);
    },
    filterData(stockData, timeFrame) {
      if (!stockData || !stockData.historical) {
        console.error('Invalid or missing stock data');
        return {};
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
          case '7D_PRED':
          // Ensure that the filter captures the entire range of the last 7 days
          startDate = moment().subtract(7, 'days').unix();
          return {
            historical: {},
            predicted: Object.fromEntries(
              Object.entries(stockData.predicted).filter(
                ([timestamp]) => timestamp >= startDate
              )
            )
          };
          case 'ALL':
          // Combine historical and predicted data, ensuring they align correctly
          return {
            historical: stockData.historical,
            predicted: Object.fromEntries(
              Object.entries(stockData.predicted).filter(
                ([timestamp]) => timestamp >= Object.keys(stockData.historical).slice(-1)[0]
              )
            ),
            performance: stockData.performance
          };
        default:
          startDate = moment().subtract(1, 'years').unix();
      }

      // Filtering logic for historical data for other cases
      return {
        historical: Object.fromEntries(
          Object.entries(stockData.historical).filter(
            ([timestamp]) => timestamp >= startDate && timestamp <= endDate
          )
        ),
        predicted: stockData.predicted
      };
    },
    calculatePerformanceData(performance, timeFrame) {
      // Extract the performance data based on the time frame
      // Assuming the performance object contains keys like '1w', '1m', etc.
      const performanceData = {};
      const timeFrameMapping = {
        '1W': '1w',
        '1M': '1m',
        '3M': '3m',
        '1Y': '1y',
        'ALL': 'all',
        '7D_PRED': '1w_predicted' // Assuming you have weekly predicted performance
      };
      const key = timeFrameMapping[timeFrame];
      performanceData[key] = performance[key];

      return performanceData;
    },
    updateTimeFrame(timeFrame) {
      this.activeTimeFrame = timeFrame; // Set the active time frame
      this.performanceData = this.calculatePerformanceData(timeFrame);
      this.createChart(this.allData, timeFrame);
    },
    async getTicker() {
      this.$store.getters.getSelectedTickerData();
    },
}, 
};
</script>

<style scoped>
caption{
  font-size: 2rem;
  caption-side: top;
}
table{
  margin: 0 auto;
  width: 100%;
  background-color: transparent;
}
#table-div-wrapper{
  padding: 0 2rem 2rem;
}
table thead th:first-child{
  border-top-left-radius: 0.5rem;
}
table thead th:last-child{
  border-top-right-radius: 0.5rem;
}
table tbody tr:nth-child(7) td:first-child{
  border-bottom-left-radius: 0.5rem;
  border: 0;
}
table tbody tr:nth-child(7) td:last-child{
  border-bottom-right-radius: 0.5rem;
  border: 0;
}
table thead th{
  padding: 1rem;
}
table tbody tr td{
  padding: 0.5rem 1rem;
}
#table-title{
  margin-left: 2rem;
}
th, td{
  background-color: #27293d;
  font-size: 1.75rem;
}
th{
  font-size: 1rem !important;
}

.chart-container, #cards{
  width: 50%;
}

.card-chart{
  padding: 0 !important;
}

#top-wrapper{
  display: flex;
  flex-direction: row;
}
#cards{
  margin-top: 2rem;
  min-width: auto; 
  min-height: auto; 
  display: grid; 
  grid-gap: 1em; 
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  padding: 2rem;
}
#cards h3{
  font-size: 2.5rem;
  margin: 0;
  margin-left: 1rem;
}
#cards h5{
  font-size: 1.25rem;
  margin: 0;
  margin-left: 1rem;
}
.card{
  margin: 0 !important;
}
@media screen and (max-width: 1050px){
  .chart-container, #cards{
    width: 100% !important;
    height: auto;
  }

  #cards{
    grid-template-columns: repeat(1fr);
    width: 100%;
  }

  #top-wrapper{
    flex-direction: column;
  }
}

#basic-info{
  margin-left: 3rem;
  h1{
    font-size: 5rem;
  }
  & > * {
    padding: 0;
    margin: 0;
    margin: 0.5rem 0;
  }
}
.overlay {
  position: absolute; /* Position overlay in relation to lineChart */
  top: 0;
  left: 0;
  width: 100%; /* Cover the full width */
  height: 100%; /* Cover the full height */
  display: flex;
  justify-content: center; /* Center the loader horizontally */
  align-items: center; /* Center the loader vertically */
  z-index: 10; /* Ensure it's above the chart */
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
  width: 100%; 
  margin: 2rem auto; 
  padding: 0; 
}


.lineChart {
  width: 100%; 
  height: auto; 
  aspect-ratio: 2 / 1; 
  position: relative;
  padding: 20px;
  box-sizing: border-box;
}

@media screen and (min-width: 1050px){
  .chart-container, #cards {
    width: 50%; 
  }
}

@media screen and (max-width: 1050px){
  #top-wrapper{
    flex-direction: column;
  }

  #cards{
    grid-template-columns: 1fr; 
    margin-top: 1rem; 
  }

  #table-div{
    overflow-x: scroll;
  }
}

.chart-controls {
  display: flex; 
  justify-content: center; 
  margin-bottom: 10px; 
  width: 100%; 
  flex-wrap: wrap; 
  padding: 10px;
  box-sizing: border-box;
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

.chart-control-button:hover,
.chart-control-button.active {
  background-color: #001eb3; 
}

.chart-control-button-7d-pred.active {
  background-color: #001eb3; 
}

.performance-data {
  font-weight: bold;
  margin-left: 8px;
}

.positive {
  font-weight: bold;
  color: rgb(0, 255, 0);
}

.negative {
  font-weight: bold;
  color: rgb(220, 1, 1);
}
.line-chart-container {
  display: flex; 
  flex-direction: column; 
  align-items: center; 
  width: 100%; 
}
</style>
