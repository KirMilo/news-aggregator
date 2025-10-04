const Header = () => {
    return (
        <div className="main-header">
            <div className="logo">Агрегатор новостей | News aggregator</div>

            <form className="search-form">
                <input
                    type="search"
                    className="search-input"
                    placeholder="Найти новость..." />
                <button type="submit" className="search-button">🔍</button>
            </form>
        </div>
    )
}

export default Header;
