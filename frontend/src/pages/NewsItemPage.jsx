import {useState, useEffect} from 'react';
import {useParams} from 'react-router';
import {useFetching} from '../hooks/useFetching';

import Header from '../components/layout/Header/Header';
import Footer from '../components/layout/Footer/Footer';
import NewsService from '../api/NewsService';
import NewsPostCategories from '../components/posts/PostList/NewsPostCategories';
// import NewsItemContent from '../components/post/NewsItemContent';
// import NewsComment from './post/NewsComment';
// import Loader from '../UI/Loader/Loader';


function NewsItemContent({post}) {
    return (
        <div className='post-content'>
            <div className='post-meta'>
                <strong>Дата публикации: {post.published_at}</strong>
            </div>
            <div className='post-title'>{post.title}</div>
            <div className='post-article'>{post.body}</div>
        </div>
    )
}


function NewsCategories({categories}) {
    return (
        <div className="news-post-item-categories">
            {categories.map(
                category =>
                    <NewsPostCategories category={category} key={category.id}/>
            )}
        </div>
    )
}


function NewsComment({user, comment}) {
    return (
        <div className='news-comment'>
            <div className='news-comment-user'>{user.username}</div>
            <div className='news-comment-content'>
                <div className='news-comment-body'>{comment.body}</div>
                <div className='news-comment-date'>{comment.published_at}</div>
            </div>
        </div>
    )
}


function CreateNewsComment({postComment}) {
    const [comment, setNewComment] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();

        if (comment.trim().length) {
            postComment(comment.trim())
        }
    }

    return (
        <form
            className="news-comment-form"
            onSubmit={handleSubmit}
        >
            <input
                className='news-comment-input'
                type="text"
                value={comment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Комментарий к новости..."
            />
            <button type="submit" className='news-comment-button'>Отправить</button>
        </form>
    )
}

function NewsComments({comments, postComment}) {
    return (
        <div className="news-comments">
            <h2>Комментарии:</h2>
            <CreateNewsComment postComment={postComment}/>
            {comments.map(
                comment =>
                    <NewsComment comment={comment} key={comment.comment.id}/>
            )
            }
        </div>
    )
}

function NewsItemPageContent() {
    const [post, setPost] = useState(undefined);
    const [comments, setComments] = useState([]);
    const [categories, setCategories] = useState([]);
    const {newsId} = useParams();
    console.log(newsId);

    const [fetchPost, isPostLoading, fetchPostError] = useFetching(
        async () => {
            const response = await NewsService.getNewsById(newsId);
            if (response.data) {
                setPost(response.data)
                setCategories(response.data.categories)
            }
        }
    )
    const [fetchComments, isCommentsLoading, fetchCommentsError] = useFetching(
        async () => {
            const response = await NewsService.getNewsComments(newsId);
            setComments(response.data);
        }
    )

    const [postComment, isPostUploading, postCommentError] = useFetching(
        async (comment) => {
            // const response = await NewsService.createNewsComment(newsId, comment);
            setComments(...comment, ...comments)
        }
    )

    useEffect(() => {
        fetchPost(newsId)
    }, [])

    if (!post) {
        return (
            <h1 style={{textAlign: 'center', marginTop: '50px'}}>Новость не найдена!</h1>
        )
    }

    return (
        <div className="news-item-content">
            <NewsCategories categories={categories}/>
            <NewsItemContent post={post}/>
            <NewsComments comments={comments} postComment={postComment}/>
        </div>
    )
}


const NewsItemPage = () => {
    return (
        <div className="app">
            <div className="news-item-container" style={{marginTop: '150px', marginLeft: '150px'}}>
                <NewsItemPageContent/>
            </div>
        </div>
    )
}

export default NewsItemPage;