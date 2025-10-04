import MainPage from "../pages/MainPage";
import NewsItemPage from "../pages/NewsItemPage";
import CategoryPage from "../pages/CategoryPage";
import SearchPage from "../pages/SearchPage";
import RegistrationPage from "../pages/RegistrationPage";
import LoginPage from "../pages/LoginPage";
import UserProfilePage from "../pages/UserProfilePage";
// import ErrorPage from "../pages/ErrorPage";


export const publicRouters = [
    { path: '/category/:categorySlug', component: CategoryPage, exact: true },
    { path: '/news/search', component: SearchPage, exact: true },
    { path: '/news/:id', component: NewsItemPage, exact: true },
    { path: '/user/register', component: RegistrationPage, exact: true },
    { path: '/user/login', component: LoginPage, exact: true },
    { path: '', component: MainPage, exact: True },

]

export const privateRouters = [
    { path: '/user/profile', component: UserProfilePage, exact: true },
]

