<template>
  <div id="app">
    <h1>Current Usage {{display_instant}}</h1>
    <br>
    <h2>Today: {{display_today}}</h2>
    <br>

    <button v-on:click="pip()">Pip</button> 
  </div>
</template>

<script>
import Utils from './Utils'

import InstantaneousAPI from './services/api/Instantaneous'
import HistoricalAPI from './services/api/Historical'

import PipAPI from './services/api/Pip'



export default {
  name: 'app',
  components: {
  },
  data(){
    return{
      powers : null,
      loading: true,
      energy_today: 0,
    }
  },
  created() {
    this.update_instant()

    setInterval(() => {
        this.update_instant()
      }, 1000);


    setInterval(() => {
        this.update_today()
      }, 10000);




    this.update_today()
  },
  methods:{
    update_instant(){
      InstantaneousAPI.listInstantaneous()
        .then(posts =>{
          this.powers = posts
        })
    },
    update_today(){
      HistoricalAPI.today()
        .then(today =>{
          this.energy_today = today.energy
        })
    },
    pip(){
      PipAPI.pip()
    }
  },
  computed: {
    display_instant(){
      if (this.powers != null) return Utils.convertWatts(this.powers["power"])
      return ""
    },
    display_today(){
      if (this.energy_today != null) return Utils.convertWh(this.energy_today)
      return ""
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
