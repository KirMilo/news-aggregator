import { useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { AuthContext } from "../context";


const RegistrationPage = () => {
    const { isAuth } = useContext(AuthContext);
    const navigate = useNavigate();

    const registration = (event) => {
        event.preventDefault();
        // localStorage.setItem('auth', 'true')
        handleBackRedirect();
        console.log("Authenticated")
    }
    const handleSubmit = (e) => {
        e.preventDefault();
    }

    const handleBackRedirect = () => {
        navigate('/auth/login', {replace: true});
    }

    useEffect(() => {
        if (isAuth) {
            navigate('/')
        }
    }, [])

    return (
        <div
            className='login-wrapper'
            onSubmit={handleSubmit}
        >

            <form className='login-form' onSubmit={registration}>
                <h2>Регистрация</h2>
                <input type="text" placeholder="username..." />
                <input type="text" placeholder="email..."/>
                <input type="password" placeholder="пароль..." />
                <input type="password" placeholder="повторите пароль..." />
                <button type="submit" className="login-button">Зарегистрироваться</button>
                <div className='register-link'>
                    <a href="/auth/login">Войти</a>
                </div>

            </form>

        </div>
    )
}

export default RegistrationPage;
