import axios from 'axios'

export default {
    pip(){
        return axios.get('/api/pip')
            .then(response => {
                return response.data
            })
    },
}

