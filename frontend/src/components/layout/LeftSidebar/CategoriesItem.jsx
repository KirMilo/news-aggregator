import { useState } from 'react';

const CategoriesItem = ({ category }) => {
    const [isOpen, setIsOpen] = useState(false);

    const hasChildren = category.children.length > 0;

    const toggleOpen = (e) => {
        e.preventDefault();
        setIsOpen(!isOpen);
    };

    return (
        <li className="news-category-item">
            <div className="news-category-header">
                <a href={`/category/${category.slug}`} className='news-category-link'>
                    {category.name}
                </a>
                {
                    hasChildren && (
                        <button
                            type="button"
                            className={`toggle-button ${isOpen ? 'open' : ''}`}
                            onClick={toggleOpen}
                            aria-expanded={isOpen}
                            aria-controls={`subcats-${category.id}`}
                        >
                            {isOpen ? '-' : '+'}
                        </button>
                    )
                }
            </div>

            { /* Подсписок вынесен изнутри header — теперь он рендерится под родительским элементом */}
            {
                hasChildren && isOpen && (
                    <ul id={`subcats-${category.id}`} className="sub-news-categories">
                        {
                            category.children.map(
                                subCategory => (
                                    <CategoriesItem key={subCategory.id} category={subCategory} />
                                )
                            )
                        }
                    </ul>
                )
            }
        </li>
    )
}

export default CategoriesItem;
