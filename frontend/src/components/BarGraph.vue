<!-- <template>
  <div id="dailyGraph">
    Daily Graph
  </div>
</template> -->

<script>

// import _ from 'lodash'

import VueCharts from 'vue-chartjs'
import { Bar, Line, mixins } from 'vue-chartjs'


export default {
  extends: Bar,
  // mixins: [mixins.reactiveProp],
  props:['labels', 'values'],
  methods:{
    draw(){
        this.renderChart({
          labels: this.labels,
          width: 100,
          height:200,
          datasets: [
            {
              label: '',
              backgroundColor: '#f87979',
              data: this.values
            }
          ]},
          {responsive: true, maintainAspectRatio:false}
        )
    }
  },
  mounted () {
    this.draw()
  },
  watch:{
    values: function (oldVal, newVal) {
        this.draw()
    }
  }
}

</script>

<style>

</style>