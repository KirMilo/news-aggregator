import NewsPostCategories from './NewsPostCategories';
import {useNavigate} from "react-router";


const NewsPostItem = (props) => {
    const navigate = useNavigate();

    const toNewsItem = e => {
        e.preventDefault();
        navigate(`/news/${props.post.id}`);
    }

    return (
        <div className="post-card" onClick={toNewsItem}>
            <div className="post-content">
                <strong className="post-title">{props.post.title}</strong>
                <hr />
                <div className="post-meta-container">
                    <div className="news-post-item-date">
                        {props.post.published_at}
                    </div>
                    <div className="news-post-item-categories">
                        {props.post.categories.map(
                            category =>
                                <NewsPostCategories category={category} key={category.id} />
                        )}
                    </div>
                </div>
            </div>

        </div>
    );
}

export default NewsPostItem;