import { useState, useEffect } from 'react'
import './styles/App.css'
import MainPage from './pages/MainPage'
import axios from 'axios'

function App() {
  const [posts, setPosts] = useState(
    [
      // { id: 1, title: "News1", body: "Description1", published_at: "01.01.2025", categories: ["Cat1", "Cat2"] },
      // { id: 2, title: "News2", body: "Description1", published_at: "01.01.2025", categories: ["Cat1", "Cat2"] },
      // { id: 3, title: "News3", body: "Description1", published_at: "01.01.2025", categories: ["Cat1", "Cat2"] }
    ]
  )
  const [categories, setCategories] = useState(
    [
      { id: 1, name: "Спорт", slug: "Sport" },
      { id: 2, name: "Экономика", slug: "Economics" },
      { id: 3, name: "Автоспорт", slug: "AutoSport" }
    ]
  )
  const [report, setReport] = useState(
    "Тут краткий отчет..."
  )

  async function fetchFreshNews() {
    const response = await axios.get('http://localhost:8001/mynews')
    // console.log(response.data)
    setPosts(response.data)
  }

  useEffect(  // Первичная подгрузка страницы
    () => {  // callback
      console.log("Use Effect")
      fetchFreshNews()
    },
    [] // Массив зависимостей
  )

  return (
    <div className="App">
      <MainPage posts={posts} categories={categories} report={report} />
    </div>
  )
}

export default App;
