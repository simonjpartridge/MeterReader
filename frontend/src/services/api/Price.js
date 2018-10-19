import axios from 'axios'

export default {
    consumptionPrice(){
        return axios.get('/api/price/consumption')
            .then(response => {
                return response.data
            })
    },
}