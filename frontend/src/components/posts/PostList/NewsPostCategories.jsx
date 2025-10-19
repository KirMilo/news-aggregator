const NewsPostCategories = ({ category }) => {
    return (
        <div className="news-item-category">
            <a
                href={`/category/${category.slug}`}
                onClick={(e) => e.stopPropagation()}
                    >{category.name}</a>
        </div>

    )
}

export default NewsPostCategories;
