import { useState, useEffect } from 'react'
import './styles/App.css'
import MainPage from './pages/MainPage'
import axios from 'axios'
import { BrowserRouter } from "react-router"

function App() {
  const [posts, setPosts] = useState([])
  const [categories, setCategories] = useState([])
  const [report, setReport] = useState(
    "Тут краткий отчет..."
  )

  async function fetchFreshNews() {
    const response = await axios.get('http://localhost:8001/api/v1/news')
    // console.log(response.data)
    setPosts(response.data)
  }

  async function fetchNewsCategories() {
    const response = await axios.get('http://localhost:8001/api/v1/news/categories')
    setCategories(response.data)
  }

  useEffect(  // Первичная подгрузка страницы
    () => {  // callback
      console.log("Use Effect")
      fetchNewsCategories()
      fetchFreshNews()
    },
    [] // Массив зависимостей
  )

  return (
    <div className="App">
      <MainPage posts={posts} categories={categories} report={report} />
    </div>
  )

  return (
    <BrowserRouter>
      <AppRouter />
    </BrowserRouter>
  )

}

export default App;
