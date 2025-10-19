import NewsPage from "../pages/NewsPage.jsx";
import NewsItemPage from "../pages/NewsItemPage";
import SearchPage from "../pages/SearchPage";
import RegistrationPage from "../pages/RegistrationPage";
import LoginPage from "../pages/LoginPage";
// import UserProfilePage from "../pages/UserProfilePage";
// import ErrorPage from "../pages/ErrorPage";


export const publicRoutes = [
    { path: '/category/:categorySlug', element: NewsPage },
    { path: '/news/search', element: SearchPage },
    { path: '/news/:newsId', element: NewsItemPage },
    { path: '/auth/registration', element: RegistrationPage},
    { path: '/auth/login', element: LoginPage },
    { path: '/', element: NewsPage },
];

// export const privateRoutes = [
//     { path: '/user/profile', component: UserProfilePage, exact: true },
// ];

