import NewsPostItem from './NewsPostItem';


const NewsPostsList = ({ posts }) => {
    return (
        <div className='news-posts-list'>
            {
                posts.map(post =>
                    <NewsPostItem post={post} key={post.id}/>
                )
            }
        </div>
    )
}

export default NewsPostsList;
