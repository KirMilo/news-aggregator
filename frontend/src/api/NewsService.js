import axios from 'axios';


const BACKEND_URL = 'http://127.0.0.1:8001/api/v1';
const NEWS_URL = BACKEND_URL + '/news';


export default class NewsService {
    static async getNewsList(offset = null, limit = 10, category = null) {
        const params = {
            limit: limit,
        }
        if (offset !== null) {
            params.offset = offset
        }
        if (category !== null) {
            params.category = category
        }
        return await axios.get(NEWS_URL, {params: params},);
    }

    static async getFreshNewsList(offset, limit = 10, category = null) {
        const params = {
            offset: offset,
            limit: limit
        }
        if (category !== null) {
            params.category = category
        }
        return await axios.get(NEWS_URL + '/fresh', {params: params},);
    }

    static async getNewsById(id) {
        return await axios.get(NEWS_URL + '/' + id);
    }

    static async getSearchNews(page = 1, limit = 10, search = '') {
        return await axios.get(
            NEWS_URL + '/search',
            {
                params: {
                    page: page,
                    limit: limit,
                    search: search,
                }
            }
        );
    }

    static async getNewsCategories() {
        return await axios.get(NEWS_URL + '/categories');
    }

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
