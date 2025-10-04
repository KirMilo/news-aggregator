import NewsPostItem from './NewsPostItem';


const NewsPostsList = ({ posts }) => {
    if (!posts.length) {
        return (
            <h1>Новости не найдены!</h1>
        )
    }

    return (
        <div>
            {
                posts.map(post =>
                    <NewsPostItem post={post} key={post.id} />
                )
            }
        </div>
    )
}

export default NewsPostsList;
