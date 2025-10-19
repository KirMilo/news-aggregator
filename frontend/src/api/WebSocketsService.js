const BACKEND_WS_URL = 'ws://127.0.0.1:8001/api/v1'


export default class WebSocketService {
    static async wsNewsUpdates(category = null, messageHandler) {
        let url = BACKEND_WS_URL + '/news/updates'
        if (category !== null) {
            url += `?category=${category}`
        }
        const socket = new WebSocket(url);

        socket.onopen = () => {
            console.log('Соединение по ws установлено!');
        };

        socket.onmessage = (event) => {
            messageHandler(JSON.parse(event.data))
        };
    }

    // static async wsCommentsUpdates(newsId = '') {
    //     const socket = await io(BACKEND_WS_URL + `/news/${newsId}/comments/updates`)
    //
    //     socket.on('connect', function () {
    //         console.log('Соединение comments updates устанолвено');
    //     })
    //
    //     socket.on('message', function (data) {
    //         console.log(`Новое сообщение comments ws ${data}`)
    //     })
    // }
}
