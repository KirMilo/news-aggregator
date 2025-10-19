import axios from 'axios';


const BACKEND_URL = 'http://127.0.0.1:8001/api/v1';
const AUTH_URL = BACKEND_URL + '/auth';


const isEmail = (login) => {
    return login.includes('@');
}

const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        throw Error('Invalid email');
    }
}

const isValidUsername = (username) => {
    const cleanName = username.trim();
    if (
        username.includes(' ')
        || username.includes('@')
        || cleanName === ''
        || cleanName.length < 2
        || cleanName.length > 15
    ) {
        throw Error(
            'Имя пользователя должно иметь длинну от 2 до 15 символов и не содержать пробелов и запрещённых символов.'
        );
    }
}

const isValidPassword = (password) => {
    if (password.length < 4) {
        throw Error('Пароль слишком короткий. Минимальная длина - 4 символа.');
    }
}

const isPasswordsEqual = (password1, password2) => {
    isValidPassword(password1);
    if (password1 !== password2) {
        throw Error('Пароли не совпадают!');
    }
}

const getLoginBody = (login, password) => {
    const body = {};
    if (isEmail(login)) {
        isValidEmail(login);
        body.email = login;
    } else {
        isValidUsername(login);
        body.username = login;
    }
    isValidPassword(password);
    body.password = password;
    return body;
}


export default class AuthService {
    static async loginUser(login, password) {
        const body = getLoginBody(login, password);
        return await axios.post(
            AUTH_URL + '/login',
            body,
        )
    }

    static async registerUser(username, email, password1, password2) {
        isValidUsername(username);
        isValidEmail(email);
        isPasswordsEqual(password1, password2);
        const body = {
            username: username,
            email: email,
            password1: password1,
            password2: password2
        }
        return await axios.post(
            AUTH_URL + '/register',
            body,
        )
    }

    static async logoutUser(refresh) {
        return axios.post(
            AUTH_URL + '/logout',
            {refresh: refresh},
        )
    }

    static async refreshToken(refresh) {
        return axios.post(
            AUTH_URL + '/token/refresh',
            {refresh: refresh},
        )
    }

    static async isAuthenticated() {
        return axios.get(
            AUTH_URL + '/user/authenticated',
            {
                withCredentials: true
            },
        )
    }
}
