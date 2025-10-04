import CategoriesItem from "../LeftSidebar/CategoriesItem";

const LeftSideBar = ({ categories }) => {
    return (
        <aside className="left-sidebar">
            <h2>Категории</h2>
            <ul className="news-categories-list">
                {
                    categories.map(category =>
                        < CategoriesItem category={category} key={category.id} />
                    )
                }
            </ul>
        </aside>
    )
}

export default LeftSideBar;
