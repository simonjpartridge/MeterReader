<template>
    <Graph  id="dailyGraph" :labels=chart_data.labels :values=chart_data.values ></Graph>
</template>

<script>

// import _ from 'lodash'

import Graph from './BarGraph'
import HistoricalAPI from '../services/api/Historical'


export default {
  components:{
    Graph
  },
  data(){
    return {
      hourly : null,
      // labels: ['1','2','3','4','5','6','7','8','9'],
      // values: [22,44,33,22,22,33,44,22,33]
    }
  },
  created(){
    this.update_chart()

    setInterval(this.update_chart, 60000)

  },
  methods:{
    update_chart(){
      HistoricalAPI.hourly()
        .then(hourly =>{
          this.hourly = hourly 
        })
    }
  },
  computed:{
    chart_data(){
      if (this.hourly == null) return {"labels": [], "values": []}

      return {"labels": this.hourly.times, "values": this.hourly.values}
    }
  }
}

</script>

<style>

#dailyGraph{
  width:100%;
  height:200px;
}

canvas{
  width:100%;
  height:100%
}

</style>