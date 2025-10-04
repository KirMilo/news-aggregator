import io from 'socket.io-client'


const BACKEND_WS_URL = 'ws://127.0.0.1:8001/api/v1'


export default class WebSocketService {
    static async wsNewsUpdates(category = '') {
        const socket = io(BACKEND_WS_URL + '/news/updates');

        socket.on('connect', function () {
            console.log('Соединение по ws установлено!');
        })

        socket.on('message', function (data) {
            console.log(`Новое сообщение ws ${data}`)
        })
    }

    static async wsCommentsUpdates(newsId = '') {
        console.log('Not implemented')
    }
}
