import CategoriesItem from "../LeftSidebar/CategoriesItem";
import {useEffect, useState} from "react";
import NewsService from "../../../api/NewsService.js";
import {useFetching} from "../../../hooks/useFetching.js";
import Loader from "../../UI/Loader/Loader.jsx";

const LeftSideBar = () => {
    const [categories, setCategories] = useState([]);

    const [fetchCategories, isCategoriesLoading, fetchCategoriesError] = useFetching(
        async () => {
            const response = await NewsService.getNewsCategories();
            setCategories(response.data);
        }
    )

    useEffect(() => {
        fetchCategories().catch(() => console.log(fetchCategoriesError));
    }, [])

    return (
        <aside className="left-sidebar">
            <h2>Категории</h2>
            {isCategoriesLoading && <Loader/>}
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
