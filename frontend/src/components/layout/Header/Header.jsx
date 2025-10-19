import {useContext, useState} from 'react';
import {useNavigate} from 'react-router';
import {AuthContext} from "../../../context/index.js";


function SearchInput() {
    const [searchTerm, setSearchTerm] = useState('');
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault(); // предотвращает перезагрузку страницы (стандартное поведение)

        if (searchTerm.trim()) {  // .trim() работает как .strip()
            navigate(`/news/search?query=${encodeURIComponent(searchTerm.trim())}`);
        }
        setSearchTerm('');  // очищает инпут
    }

    return (
        <div className='search-form-box'>
            <form
                className='search-form'
                onSubmit={handleSubmit}
            >
                <input
                    className='search-input'
                    type="search"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    placeholder="Найти новость..."
                />
                <button type="submit" className="search-button">🔍</button>
            </form>
        </div>
    )
}


function ProfileLogout() {
    const {isAuth, isLoading} = useContext(AuthContext);

    return (
        <div className='profile-logout-wrapper'>
            {
                isAuth ?
                    <div>
                        <a href='/user/1'>Имя профиля</a>
                        &nbsp;|&nbsp;
                        <a href='/auth/logout'>logout</a>
                    </div>
                    :
                    <div>
                        <a href='/auth/login'>вход</a>
                        &nbsp;|&nbsp;
                        <a href='/auth/register'>регистрация</a>
                    </div>
            }
        </div>)
}


const Header = () => {
    // Использовать условный рендеринг, то есть если пользователь авторизован отрисовываем профиль и аватарку
    // В противном случае вход или регистрация {isAuth ? часть где авторизован : не авторизован}
    return (
        <div className="main-header">
            <div className='logo-box'>
                <a className="logo" href="/">
                    Агрегатор новостей | News aggregator
                </a>

            </div>
            <SearchInput/>
            <ProfileLogout/>
        </div>
    )
}

export default Header;
