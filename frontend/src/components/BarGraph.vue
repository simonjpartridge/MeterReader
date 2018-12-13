<!-- <template>
  <div id="dailyGraph">
    Daily Graph
  </div>
</template> -->

<script>

// import _ from 'lodash'

// import VueCharts from 'vue-chartjs'
import { Bar } from 'vue-chartjs'


export default {
  extends: Bar,
  props:['labels', 'values'],
  methods:{
    draw(){
        this.renderChart({
          labels: this.labels,
          width: 100,
          height:200,
          title:{
            display:false,
          },
          datasets: [
            {
              label: '',
              backgroundColor: '#f87979',
              data: this.values
            }
          ]},
          {
            responsive: true, 
            maintainAspectRatio:false,
            legend:{
                display:false,
            },
            animation:{
                duration:0
            }
          }
        )
    }
  },
  mounted () {
    this.draw()
  },
  watch:{
    values: function () {
        this.draw()
    }
  }
}

</script>

<style>

</style>