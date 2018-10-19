export default {
    convertWh(watt_hours){
        if (watt_hours > 500){
            return (watt_hours/1000.0).toFixed(1) + " kWh"
        }else{
            return Math.ceil(watt_hours.toFixed(0) / 10) * 10 + " Wh"
        }
    },

    convertWatts(watts){
        if (watts > 500){
            return (watts/1000.0).toFixed(1)  + " Kw"
        }else{
            return Math.ceil(watts.toFixed(0) / 10) * 10 + " W"
        }
    },
}