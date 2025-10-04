


function Posts() {
    const [posts, setPosts] = useState([]);
    const [aiReport, setAiReport] = useState('');
    const [categories, setCategories] = useState([]);

    const [page, setPage] = useState(1);
    const [limit, setLimit] = useState(10);
    const [isLastPage, setIsLastPage] = useState(false);
    const [isNewsPosts, setIsNewPosts] = useState(false);
    const lastElement = useRef();
    const firstElement = useRef();
    const { categorySlug } = useParams();

    console.log(`Slug категории: ${categorySlug}`);

    const [fetchPosts, isPostsLoading, fetchPostsError] = useFetching(
        async (categorySlug, limit, page) => {
            const response = await NewsService.getNewsList(categorySlug, limit, page);
            setPosts([...posts, ...response.data.data])
        }
    )

    const [fetchCategories, isCategoriesLoading, fetchCategoriesError] = useFetching(
        async () => {
            const response = await NewsService.getNewsCategories();
            setCategories(response.data);
        }
    )

    useEffect(() => {
        fetchPosts(categorySlug, limit, page)
        fetchCategories()
        setAiReport(`Краткий отчет категории: ${categorySlug}`)
    }, [categorySlug, limit, page])
}