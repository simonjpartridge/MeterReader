import axios from 'axios'

export default {
    listInstantaneous(){
        return axios.get('/api/instantaneous')
            .then(response => {
                return response.data
            })
    },
}

