import {useEffect, useState} from 'react';
import {useSearchParams} from 'react-router';

import {useFetching} from '../hooks/useFetching';
import NewsService from '../api/NewsService';
import Header from '../components/layout/Header/Header';
import Footer from '../components/layout/Footer/Footer';


const FoundItem = ({item}) => {
    return (
        <div className='post-card'>
            <div className='post__content'>
                <strong className='post-title'>{item.title}</strong>
                <div className='post-meta-container'>
                    {item.published_at}
                </div>
            </div>
        </div>
    )
}


const FoundResults = ({items}) => {
    // if (!items.length) {
    //     return <h1 style={{textAlign: 'center', marginTop: '50px'}}>Посты не найдены!</h1>
    // }

    return (
        <div>
            {
                items.map(item =>
                    <FoundItem item={item} key={item.id}/>
                )
            }
        </div>
    )
}


const SearchPage = () => {
    const [searchParams] = useSearchParams();
    const query = searchParams.get('query');
    const [results, setResults] = useState([]);

    const [page, setPage] = useState(1);
    const [limit, setLimit] = useState(10);


    const [fetchResults, isResultsLoading, fetchResultsError] = useFetching(
        async (query, limit, page) => {
            if (query.length >= 3) {
                const response = await NewsService.getSearchNews(query, limit, page);
                console.log(response.data)
                setResults(response.data)
            }
        }
    )

    useEffect(() => {
        fetchResults(query, page, limit);
    }, [])


    return (
        <div className='search-page-container'>
            <FoundResults items={results}/>
        </div>
    )
}

export default SearchPage;
