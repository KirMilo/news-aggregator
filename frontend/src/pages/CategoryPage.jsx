import { useState, useRef } from 'react';
import { useParams } from 'react-router-dom';

import Header from '../components/layout/Header/Header';
import Footer from '../components/layout/Footer/Footer';
import AiReportBlock from '../components/posts/AiSection/AiReport';
import LeftSideBar from '../components/layout/LeftSideBar';

import { useFetching } from '../hooks/useFetching';
import NewsService from '../api/NewsService';


function CategoryPage() {
    const [posts, setPosts] = useState([]);
    const [aiReport, setAiReport] = useState('');
    const [categories, setCategories] = useState([]);

    const [page, setPage] = useState(1);
    const [limit, setLimit] = useState(10);
    const [isLastPage, setIsLastPage] = useState(false);
    const [isNewsPosts, setIsNewPosts] = useState(false);
    const lastElement = useRef();
    const firstElement = useRef();
    const { categorySlug } = useParams();

    console.log(`Slug категории: ${categorySlug}`);

    const [fetchPosts, isPostsLoading, fetchPostsError] = useFetching(
        async (categorySlug, limit, page) => {
            const response = await NewsService.getNewsList(categorySlug, limit, page);
            setPosts([...posts, ...response.data.data])
        }
    )

    const [fetchCategories, isCategoriesLoading, fetchCategoriesError] = useFetching(
        async () => {
            const response = await NewsService.getNewsCategories();
            setCategories(response.data);
        }
    )

    useEffect(() => {
        fetchPosts(categorySlug, limit, page)
        fetchCategories()
        setAiReport(`Краткий отчет категории: ${categorySlug}`)
    }, [categorySlug, limit, page])


    return (
        <div className='mainpage-container'>
            <Header />
            <div className='left-side-bar'>
                <LeftSideBar categories={categories} />
            </div>
            <div className='main-content'>
                <div className='posts-section'>
                    <AiReportBlock report={aiReport} />
                    <NewsPostsList posts={posts} />
                </div>
            </div>
            <Footer />
        </div>
    )
}

export default CategoryPage;