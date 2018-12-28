import axios from 'axios'

export default {
    pip(){
        var timestamp = (new Date).getTime() / 1000.0
        return axios.get('/api/pip/' + timestamp )
            .then(response => {
                return response.data
            })
    },
}

