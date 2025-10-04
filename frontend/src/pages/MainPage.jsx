// import React from 'react';
import Header from '../components/layout/Header/Header';
import Footer from '../components/layout/Footer/Footer';
import NewsPostsList from '../components/posts/PostList/NewsPostsList';
import AiReportBlock from '../components/posts/AiSection/AiReport';
import LeftSideBar from '../components/layout/LeftSideBar/LeftSideBar';


function NewsList(category = '') {
    const [posts, setPosts] = useState([]);
    const [page, setPage] = useState(1);
    const [limit, setLimit] = useState(10);
    const [isLastPage, setIsLastPage] = useState(false);
    const [isNewPosts, setIsNewPosts] = useState(false);
    const lastElement = useRef();

    const [fetchPosts, isPostsLoading, postError] = useFetching(async (category, limit, page) => {
        const response = await NewsService.getNewsList(category, limit, page);
        setPosts([...posts, ...response.data.data])
    })

    // useObserver

    useEffect(() => {
        fetchPosts(category, limit, page)
    }, [category, limit, page])
}


const MainPage = ({ posts, categories, report }) => {
    return (
        <div className="mainpage-container">
            <Header />
            <div className="left-side-bar">
                <LeftSideBar categories={categories} />
            </div>
            <div className="main-content">
                <div className="posts-section">
                    <AiReportBlock report={report} />
                    <NewsPostsList posts={posts} />
                </div>
            </div>
            <Footer />
        </div>
    )
}

export default MainPage;