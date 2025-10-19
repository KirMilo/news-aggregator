import {useEffect, useState} from 'react';


function isActiveCategory(children, activeCat) {
    let queue = [...children]
    while (queue.length) {
        let left = queue.shift()
        if (left.slug === activeCat) {
            return true;
        }
        queue = [...queue, ...left.children]
    }
    return false;
}


const CategoriesItem = ({category, activeCat}) => {
    const [isOpen, setIsOpen] = useState(false);
    const [isActive, setIsActive] = useState(false);

    const hasChildren = category.children.length > 0;

    const toggleOpen = (e) => {
        e.preventDefault();
        setIsOpen(!isOpen);
    };

    useEffect(() => {
        if (isActiveCategory(category.children, activeCat)) {
            setIsOpen(true);
            setIsActive(true);
        }
    }, [])

    return (
        <li className="news-category-item">
            <div className="news-category-header">
                <a
                    href={`/category/${category.slug}`}
                    className={activeCat === category.slug ? 'news-category-link-active' : 'news-category-link'}
                >
                    {category.name}
                </a>
                {
                    hasChildren && !isActive && (
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

            {
                hasChildren && isOpen && (
                    <ul className="sub-news-categories">
                        {
                            category.children.map(
                                subCategory => (
                                    <CategoriesItem
                                        key={subCategory.id}
                                        category={subCategory}
                                        activeCat={activeCat}
                                    />
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
