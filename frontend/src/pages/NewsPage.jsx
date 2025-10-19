import {useState, useRef, useEffect} from 'react';
import {useParams} from 'react-router';

import NewsPostsList from '../components/posts/PostList/NewsPostsList';
import AiReportBlock from '../components/posts/AiSection/AiReport';
import LeftSideBar from '../components/layout/LeftSideBar/LeftSideBar';
import {useFetching} from '../hooks/useFetching';
import NewsService from '../api/NewsService';
import Loader from '../components/UI/Loader/Loader';
import {useObserver} from "../hooks/useObserver.js";
import WebSocketService from "../api/WebSocketsService.js";
import FreshNewsCount from "../components/posts/FreshNewsBlock/FreshNewsCountSectioin.jsx";


async function newsUpdates(setFreshNewsCount, setPosts, category, setIsUpdating) {
    const handleNewsUpdate = (newsId) => {
        console.log(`News updated for ${newsId}`);
    }

    const handleNewWSMessage = ({action, value}) => {
        setIsUpdating(true);
        switch (action) {
            case 'new':
                setFreshNewsCount((prev) => prev + value);
                break;
            case 'delete':
                setPosts((posts) => [...posts.filter((post) => post.id !== value)])
                console.log(`News with id ${value} has been deleted`)
                setIsUpdating(false);
                break;
            case 'update':
                handleNewsUpdate(value);
                console.log(`update ${value}`);
                break;
            default:
                break;
        }
        setIsUpdating(false);
    }

    await WebSocketService.wsNewsUpdates(category, handleNewWSMessage);
}


const LoadFreshNews = ({freshNewsCount, setFreshNewsCount, setPosts, offset, setOffset, limit, category}) => {
    const firstElement = useRef(null);

    const [fetchPosts, isPostsLoading, fetchPostsError] = useFetching(
        async () => {
            const response = await NewsService.getFreshNewsList(offset, limit, category);
            const {data, next} = response.data;
            setPosts((prev) => [...data, ...prev])
            setOffset(next)
            setFreshNewsCount((prev) => Math.max(prev - data.length, 0))
        }
    )

    useEffect(() => {
        if (!firstElement.current || freshNewsCount <= 0) return;

        const callback = (entries) => {
            if (entries[0].isIntersecting && freshNewsCount > 0) {
                fetchPosts();
                if (fetchPostsError) {
                    console.log(fetchPostsError);
                }
            }
        };
        const observer = new IntersectionObserver(callback, {threshold: 0.1})
        observer.observe(firstElement.current)
        return () => {observer.disconnect();}
    }, [freshNewsCount, offset])

    return (
        <div>
            <div ref={firstElement} style={{height: 2}}>
                {isPostsLoading && <Loader/>}
            </div>

        </div>
    )
}


const LoadOldNews = ({setPosts, offset, setOffset, limit, category, setIsOldPosts}) => {
    const lastElement = useRef(null);

    const [fetchPosts, isPostsLoading, fetchPostsError] = useFetching(
        async () => {
            const response = await NewsService.getNewsList(offset, limit, category);
            const data = response.data.data
            const next = response.data.next
            setPosts((prev) => [...prev, ...data])
            setOffset(next)
            }
        )

    useObserver(lastElement, true, isPostsLoading, () => {
            fetchPosts();
            if (fetchPostsError) {
                setIsOldPosts(false);
            }
        }
    )

    return (
        <div ref={lastElement} style={{height: 0}}>
            {
                isPostsLoading &&
                <div style={{position: 'sticky', paddingBottom: '80px'}}>
                    <Loader/>
                </div>
            }
        </div>
    )
}


const NewsPage = () => {
    const [posts, setPosts] = useState([]);
    const [aiReport, setAiReport] = useState(null);

    const [lowerOffset, setLowerOffset] = useState(null);
    const [upperOffset, setUpperOffset] = useState(null);
    const limit = 10;
    const {categorySlug} = useParams();

    const [isOldPosts, setIsOldPosts] = useState(false);
    const [isUpdating, setIsUpdating] = useState(false);
    const [freshNewsCount, setFreshNewsCount] = useState(0);


    const [fetchPosts, isPostsLoading, fetchPostsError] = useFetching(
        async () => {
            const response = await NewsService.getNewsList(lowerOffset, limit, categorySlug);
            const {next, previous, data} = response.data;
            setPosts([...posts, ...data])
            setLowerOffset(next)
            setUpperOffset(previous)
            if (data.length >= limit) {
                setIsOldPosts(true);
            }
        }
    )

    const [fetchAiReport, isAiReportLoading, fetchAiReportError] = useFetching(
        async (category) => {
            setAiReport(`Краткий отчет категории: ${category}`);
        }
    )

    useEffect(() => {
        fetchPosts();
        fetchAiReport();
        newsUpdates(setFreshNewsCount, setPosts, categorySlug, setIsUpdating);
    }, []);

    const scrollToTop = () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    };

    return (
        <div className="app">
            <div className="left-side-bar">
                <LeftSideBar/>
            </div>
            <div className="main-content">
                <div className="posts-section">
                    {
                        fetchPostsError
                            ?
                            <div style={{marginLeft: '250px'}}>
                                <h2 style={{minWidth: '260px'}}>Новости не найдены!</h2>
                            </div>
                            :
                            <div>
                                {freshNewsCount > 0 &&
                                    <FreshNewsCount count={freshNewsCount} onClick={scrollToTop}/>
                                }
                                <AiReportBlock report={aiReport}/>
                                <LoadFreshNews
                                    freshNewsCount={freshNewsCount}
                                    setFreshNewsCount={setFreshNewsCount}
                                    setPosts={setPosts}
                                    offset={upperOffset}
                                    setOffset={setUpperOffset}
                                    limit={limit}
                                    category={categorySlug}
                                />
                                <hr></hr>
                                <NewsPostsList posts={posts}/>
                                {(isOldPosts && !isUpdating) && <LoadOldNews
                                    setPosts={setPosts}
                                    offset={lowerOffset}
                                    setOffset={setLowerOffset}
                                    limit={limit}
                                    category={categorySlug}
                                    setIsOldPosts={setIsOldPosts}
                                />}
                            </div>
                    }
                </div>
            </div>
            {(isPostsLoading || isAiReportLoading) && <Loader/>}
        </div>
    )
}


export default NewsPage;
