import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
    /* выключить строгий режим, вызывает двойную отрисовку */
    // <StrictMode>
        <App/>
    //</StrictMode>
)
