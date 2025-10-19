import CategoriesItem from "../LeftSidebar/CategoriesItem";

const LeftSideBar = ({categories, activeCat}) => {
    return (
        <aside className="left-sidebar">
            <h2>Категории</h2>
            <ul className="news-categories-list">
                {
                    categories.map(category =>
                        < CategoriesItem
                            key={category.id}
                            category={category}
                            activeCat={activeCat}
                        />
                    )
                }
            </ul>
        </aside>
    )
}

export default LeftSideBar;
