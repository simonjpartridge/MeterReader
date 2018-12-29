import axios from 'axios'

export default {
    today(){
        return axios.get('/api/total/today')
            .then(response => {
                return response.data
            })
    },
    last24(){
        return axios.get('/api/total/last24')
            .then(response => {
                return response.data
            })
    },
    hourly(){
        return axios.get('/api/historical/hourly/today')
            .then(response => {
                return response.data
            })
    },
    daily(){
        return axios.get('/api/historical/daily/last30')
            .then(response => {
                return response.data
            })
    }
}