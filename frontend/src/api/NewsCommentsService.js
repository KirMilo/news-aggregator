import axios from "axios";

const BACKEND_URL = 'http://127.0.0.1:8001/api/v1';
const NEWS_URL = BACKEND_URL + '/news';

export default class NewsCommentsService {
    static async getNewsComments(newsId) {
        return await axios.get(NEWS_URL + `/${newsId}/comments`);
    }

    static async createNewsComment(newsId, comment) {
        return await axios.post(
            NEWS_URL + `/${newsId}/comment`,
            {
                withCredentials: true,
                news_id: {newsId},
                body: {comment},
            }
        );
    }
}