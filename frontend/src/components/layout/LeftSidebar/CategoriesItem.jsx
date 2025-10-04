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
                <a href={`/category/${category.slug}`} className={`news-category-link ${hasChildren ? 'has-children' : ''}`}>
                    {category.name}
                </a>
                {
                    hasChildren && (
                        <button className={`toggle-button ${isOpen ? 'open' : ''}`} onClick={toggleOpen} aria-expanded={isOpen} aira-controls={`sublist-${category.id}`}>
                            {isOpen ? '-' : '+'}
                        </button>
                    )
                }
                {
                    hasChildren && isOpen && (
                        <ul id={`subcats-${category.id}`} className="sub-news-category">
                            {
                                category.children.map(
                                    subCategory => (
                                        < CategoriesItem key={subCategory.id} category={subCategory} />
                                    )
                                )
                            }
                        </ul>
                    )
                }
            </div>
        </li>
    )
}

export default CategoriesItem;
