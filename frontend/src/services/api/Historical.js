import axios from 'axios'

export default {
    today(){
        return axios.get('/api/historical/today')
            .then(response => {
                return response.data
            })
    },
    last24(){
        return axios.get('/api/historical/last24')
            .then(response => {
                return response.data
            })
    },
    hourly(){
        return axios.get('/api/historical/hourly/today')
            .then(response => {
                return response.data
            })
    }
}