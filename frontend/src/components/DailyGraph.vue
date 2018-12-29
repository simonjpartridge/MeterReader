<template>
  <div id="dailyGraphContainer">
    <Graph  id="dailyGraph" :labels=chart_data.labels :values=chart_data.values ></Graph>
    <div v-on:click="toggleView">Toggle</div>
  </div>
</template>

<script>

import Graph from './BarGraph'
import HistoricalAPI from '../services/api/Historical'


export default {
  components:{
    Graph
  },
  data(){
    return {
      hourly : null,
      daily: null,
      toShow: "hourly"
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
      
      HistoricalAPI.daily()
        .then(daily =>{
          this.daily = daily 
        })
    },
    toggleView(){
      if (this.toShow =="daily"){
        this.toShow="hourly"
      }else{
        this.toShow="daily"
      }

    }
  },
  computed:{
    chart_data(){
      if (this.toShow == "hourly"){
        if (this.hourly == null) return {"labels": [], "values": []}
  
        var hours = this.hourly.times.map(hour => hour.split(" ")[1].split(":")[0]) //parse to get just hour entry
  
        return {"labels": hours, "values": this.hourly.values}
      }else if(this.toShow == "daily"){
        if (this.daily == null) return {"labels": [], "values": []}

        var days = this.daily.times.map(day => day.split(" ")[0].split("-")[2]) //parse to get just hour entry

        return {"labels": days, "values": this.daily.values}
      }
    }
  }
}

</script>

<style>

#dailyGraph{
  width:100%;
  height:200px;
  max-width:500px;
  margin-left:auto;
  margin-right:auto;
}

#dailyGraphContainer{
  text-align:center
}

canvas{
  width:100%;
  height:100%
}

</style>