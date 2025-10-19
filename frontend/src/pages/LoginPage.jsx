import {useContext, useState, useEffect} from 'react';
import {useNavigate} from 'react-router';
import {AuthContext} from "../context";
import PasswordInput from "../components/UI/input/Password";


const LoginPage = () => {
    const {isAuth, setIsAuth} = useContext(AuthContext);
    const navigate = useNavigate();

    const login = (event) => {
        event.preventDefault();
        setIsAuth(true);
        localStorage.setItem('auth', 'true')
        // handleBackRedirect();
        console.log("Authenticated")
    }
    const handleSubmit = (e) => {
        e.preventDefault();
    }

    const handleBackRedirect = () => {
        if (document.referrer !== '' && document.referrer.lastIndexOf('/auth/registration') === -1) {
            navigate(-1);
        } else {
            navigate('/', {replace: true});
        }
    }

    useEffect(() => {
        if (isAuth) {
            handleBackRedirect();
        }
    }, [isAuth])
    const [showPassword, setShowPassword] = useState(false)
    return (

        <div
            className='login-wrapper'
            onSubmit={handleSubmit}
        >
            <form className='login-form' onSubmit={login}>
                <h2>Вход</h2>
                <input type="text" placeholder="логин или email..."/>
                <PasswordInput placeholder="пароль"/>
                <button type="submit" className="login-button">Войти</button>
                <div className='register-link'>
                    <a href="/auth/registration">Регистрация</a>
                </div>
                <div className='register-link'>
                    <a href="/auth/forgot">Забыли пароль?</a>
                </div>
            </form>

        </div>
    )
}

export default LoginPage;
