<script>
import {Line} from "vue-chartjs";
export default{
    extends: Line,
    props: {
        label: {
            type: String
        },
        chartData: {
            type: Array
        },
        options: {
            type: Object
        },
        chartColors: {
            type: Object
        }
    },
    mounted() {
        const stock = this.chartData.map(d => d.stockSymbol).reverse;
        const currentPrice = this.chartData.map(d => d.currentPrice).reverse();
        
        const {
            borderColor,
            pointBorderColor,
            pointBackgroundColor,
            backgroundColor
        } = this.chartColors;

        this.renderChart({
            labels: stock,
            datasets: [
                {
                    label : this.label,
                    data: currentPrice,
                    borderColor: borderColor,
                    pointBorderColor: pointBorderColor,
                    pointBackgroundColor: pointBackgroundColor,
                    backgroundColor: backgroundColor
                }
            ]
        },
        this.options
        );
    }
}
</script>