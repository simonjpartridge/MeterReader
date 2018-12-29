<template>
  <div id="app">
    <div class="instant">Current {{display_instant}}</div>
    <div class="today">Today: {{display_today}} / £{{display_today_cost}} </div>
    <DailyGraph></DailyGraph>

    <button v-on:click="pip()">Pip</button> 
  </div>
</template>

<script>
import Utils from './Utils'

import DailyGraph from './components/DailyGraph'

import InstantaneousAPI from './services/api/Instantaneous'
import HistoricalAPI from './services/api/Historical'
import PriceAPI from './services/api/Price'
import PipAPI from './services/api/Pip'



export default {
  name: 'app',
  components: {
    DailyGraph
  },
  data(){
    return{
      powers : null,
      loading: true,
      energy_today: 0,
      consumption_price: 0
    }
  },
  created() {
    this.update_instant()
    this.get_consumption_prices()
    this.update_today()

    setInterval(() => {
        this.update_instant()
      }, 2000);


    setInterval(() => {
        this.update_today()
      }, 20000);

    setInterval(() => {
      this.refresh()
      }, 1000000);




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
    refresh(){
      location.reload();
    },
    pip(){
      PipAPI.pip()
    },
    get_consumption_prices(){
      PriceAPI.consumptionPrice()
        .then(data =>{
          this.consumption_price = data.price
        })
    }
  },
  computed: {
    display_instant(){
      if (this.powers != null) return Utils.convertWatts(this.powers["power"])
      return "0"
    },
    display_today(){
      if (this.energy_today != null) return Utils.convertWh(this.energy_today)
      return "0"
    },
    display_today_cost(){
      if (this.energy_today != null) return (this.energy_today/1000 * this.consumption_price).toFixed(2)
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
  margin-top: 0px;
}

.instant{
  font-size:1.4em
}

.today{
  font-size:1.2em
}
</style>
