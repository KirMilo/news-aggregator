

const FreshNewsCount = ({count, ...props}) => {

    return (
        <div {...props} className="fresh-news-count-section">
            <div className="fresh-news-sliding-panel">
                Опубликовано новостей: {count}...
            </div>
        </div>
    )
}


export default FreshNewsCount;