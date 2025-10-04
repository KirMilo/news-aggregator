import { useEffect, useState, useParams } from 'react';
import Header from '../components/layout/Header/Header';
import Footer from '../components/layout/Footer/Footer';
// import NewsPostsList from '../components/posts/PostList/NewsPostsList';
// import AiReportBlock from '../components/posts/AiSection/AiReport';
// import LeftSideBar from '../components/layout/LeftSideBar/LeftSideBar';


const NewsItemPage = () => {
    const params = useParams();
    const [post, setPost] = useState({});
    // const [comments, setComments] = useState([]);
    const [fetchNewsById, isLoading, error] = useFetching(async (id) => {
        const response = await PostService.getById(id)
        setPost(response.data);
    })
    // const [fetchComments, isCommentsLoading, commentsError] = useFetching(async (id) => {
    //     const response = await PostService.getCommentsByNewsId(id)
    //     setComments(response.data);
    // })

    useEffect(
        () => {
            fetchNewsById(params.id)
            // fetchComments(params.id)
            // Установить сюда сокет комментов
        }, []
    )

    return (
        <div className="news-item-page">
            {
                isLoading ? <Loader /> : <div>
                    {/* Доделать категории и дата публикации! */}
                    <h1>{post.title}</h1>
                    <h2>{post.body}</h2>
                </div>
            }
            <div>
                <h5>Здесь будут комментарии!</h5>
            </div>
        </div>
    )
}

export default NewsItemPage;