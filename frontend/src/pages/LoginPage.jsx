import { useContext } from 'react';
import { AuthContext } from "../context";


const Login = () => {
    const { isAuth, setIsAuth } = useContext(AuthContext);

    const login = event => {
        event.preventDefault();
        setIsAuth(true);
        localStorage.setItem('auth', 'true')
    }

    return (
        <div>
            <h1>Авторизация</h1>
            <form onSubmit={login}>
                <input type="text" placeholder="логин или email..." />
                <input type="password" placeholder="пароль" />
                <Button>Войти</Button>
            </form>
            <Button>Регистрация</Button>
        </div>
    )
}

export default Login;
