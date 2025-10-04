import axios from 'axios';


const BACKEND_URL = 'http://127.0.0.1:8001/api/v1';
const NEWS_URL = BACKEND_URL + '/news';


export default class NewsService {
    static async getNewsList(category = '', limit = 10, page = 1) {
        const params = {
            limit: limit,
            page: page,
        }
        if (category !== '') {
            params.category = category
        }

        const response = await axios.get(NEWS_URL, { params: params },)
        return response;
    }

    static async getNewsById(id) {
        const response = await axios.get(NEWS_URL + '/' + id)
        return response;
    }

    static async getSearchNews(limit = 10, page = 1, search) {
        const response = await axios.get(
            NEWS_URL + '/search',
            {
                params: {
                    limit: limit,
                    page: page,
                    search: search,
                }
            }
        )
        return response;
    }

    static async getNewsCategories() {
        const response = await axios.get(NEWS_URL + '/categories')
        return response;
    }
}

