import './styles/App.css'
import {useEffect, useState} from 'react';
import {BrowserRouter} from "react-router";
import AppRouter from './components/AppRouter';
import {AuthContext} from './context';
import Header from "./components/layout/Header/Header.jsx";
import Footer from "./components/layout/Footer/Footer.jsx";

function App() {
    const [isAuth, setIsAuth] = useState(false);
    const [isLoading, setLoading] = useState(true);

    useEffect(() => {
        if (localStorage.getItem('auth')) {
            setIsAuth(true)
        }
        setLoading(false);
    }, [])

    return (
        <AuthContext.Provider value={
            {
                isAuth,
                setIsAuth,
                isLoading
            }
        }>
            <BrowserRouter>
                <Header />
                <AppRouter/>
                <Footer />
            </BrowserRouter>
        </AuthContext.Provider>
    )
}

export default App;
