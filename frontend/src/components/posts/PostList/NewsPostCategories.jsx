const NewsPostCategories = ({ category }) => {
    return (
        <div className="news-item-category" onClick={(e) => e.stopPropagation()}>
            <a
                href={`/category/${category.slug}`}
                    >{category.name}</a>
        </div>

    )
}

export default NewsPostCategories;
