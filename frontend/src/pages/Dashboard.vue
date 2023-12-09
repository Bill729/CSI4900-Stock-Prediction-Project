<template>
  <div>
    <div id="top-wrapper">
      <div class="chart-container" v-if="selectedStock">
        <div id="basic-info" v-if="this.$store.getters.getSelectedTickerData().name">
          <h1>${{ this.$store.getters.getSelectedTickerData().info.currentPrice }}</h1>
          <h2>{{ this.$store.getters.getSelectedTickerData().info.companyName }}</h2>
        </div>
        <div class="chart-controls">
          <button :class="['chart-control-button', '1W' === activeTimeFrame ? 'active' : '']" @click="updateTimeFrame('1W')">1W</button>
          <button :class="['chart-control-button', '1M' === activeTimeFrame ? 'active' : '']" @click="updateTimeFrame('1M')">1M</button>
          <button :class="['chart-control-button', '3M' === activeTimeFrame ? 'active' : '']" @click="updateTimeFrame('3M')">3M</button>
          <button :class="['chart-control-button', '1Y' === activeTimeFrame ? 'active' : '']" @click="updateTimeFrame('1Y')">1Y</button>
          <button :class="['chart-control-button', 'ALL' === activeTimeFrame ? 'active' : '']" @click="updateTimeFrame('ALL')">ALL</button>
          <button :class="['chart-control-button', 'chart-control-button-7d-pred', '7D_PRED' === activeTimeFrame ? 'active' : '']" @click="updateTimeFrame('7D_PRED')">7D Predicted</button>
        </div>
        <div class="lineChart">
          <canvas id="myChart"></canvas>
          <div v-if="loading" class="overlay">
            <div class="loader"></div>
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
    <h2>Model Performance (7D Predicted)</h2>
    <div style="overflow-x: scroll;" id="table-div">
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
              <td>{{ formatDecimalNumber(el[1]['MAE'], 4) }}</td>
              <td>{{ formatDecimalNumber(el[1]['MSE'], 4) }}</td>
              <td>{{ formatDecimalNumber(el[1]['RMSE'], 4) }}</td>
            </tr>
            <tr></tr>
          </tbody>
        </table>
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
      predictedModelPerformance: []
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
        }
      }
    });
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
            )
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
    updateTimeFrame(timeFrame) {
      this.activeTimeFrame = timeFrame; // Set the active time frame
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
}
#cards h3{
  font-size: 2rem;
  margin: 0;
  margin-left: 1rem;
}
#cards h5{
  font-size: 1rem;
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
  position: absolute; /* Positioned absolutely to the parent relative container */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10; /* Ensure it's above other content */
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
  margin: 2rem 0;
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
  margin-left: 140px;
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
.chart-control-button.active { /* Add .active here */
  background-color: #001eb3; /* This color will show on hover and when the button is active */
}

/* Specific style for the '7D Pred' button when it is active */
.chart-control-button-7d-pred.active {
  background-color: #ff4500; /* Same color as the border color for the '7D Pred' button */
}
</style>
