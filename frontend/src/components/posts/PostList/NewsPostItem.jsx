import NewsPostCategories from './NewsPostCategories';


const NewsPostItem = (props) => {
    return (
        <div className="post-card">
            <div className="post__content">
                <strong className="post-title">{props.post.title}</strong>
                <div className="news-post-item-body post-content">
                    {props.post.body}
                </div>
                <div className="post-meta-container">
                    <div className="news-post-item-date">
                        {props.post.published_at}
                    </div>
                    <div className="news-post-item-categories">
                        {props.post.categories.map(
                            category =>
                                <NewsPostCategories category={category} key={category} />
                        )}
                    </div>
                </div>
            </div>
            <hr />
        </div>
    );
}

export default NewsPostItem;