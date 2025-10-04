import { useContext } from 'react';
import { Routes, Route, Navigate } from 'react-router';
import { privateRoutes, publicRoutes } from '../router';
import { AuthContext } from '../context';
import Loader from "./UI/Loader/Loader";


const AppRouter = () => {
    const { isAuth, isLoading } = useContext(AuthContext);
    console.log(isAuth)

    if (isLoading) {
        return <Loader />
    }

    return (
        // isAuth
        //     ?
        //     <Routes>
        //         {privateRoutes.map(route =>
        //             <Route
        //                 component={route.component}
        //                 path={route.path}
        //                 exact={route.exact}
        //                 key={route.path}
        //             />
        //         )}
        //         <Navigate to='/user/login' />
        //     </Routes>
        //     :
        <Routes>
            {publicRoutes.map(route =>
                <Route
                    component={route.component}
                    path={route.path}
                    exact={route.exact}
                    key={route.path !== '' ? route.path : '/mainpage'}
                />
            )}
            <Navigate to='' />
        </Routes>
    )
}

export default AppRouter;
