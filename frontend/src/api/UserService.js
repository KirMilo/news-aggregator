import axios from 'axios';


const BACKEND_URL = 'http://127.0.0.1:8001/api/v1';
const USER_URL = BACKEND_URL + '/user';


export default class UserService {
    static async getUser(user_id) {
        return await axios.get(
            USER_URL + `/${user_id}`,
            {
                withCredentials: true,
            }
        )
    }

    static async postAvatar(formData) {
        return await axios.post(
            USER_URL + '/avatar',
            formData,
            {
                withCredentials: true,
            }
        )
    }
}
