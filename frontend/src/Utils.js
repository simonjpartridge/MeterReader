

export default {
    convertWh(watt_hours){
        if (watt_hours > 500){
            return (watt_hours/1000.0).toFixed(2) + " kWh"
        }else{
            return watt_hours.toFixed(0) + " Wh"
        }
    },

    convertWatts(watts){
        if (watts > 500){
            return (watts/1000.0).toFixed(2) + " Kw"
        }else{
            return watts.toFixed(0) + " W"
        }
    }
    
}