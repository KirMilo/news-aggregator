from aiohttp import ClientSession
from typing import AsyncGenerator

# Инициализация БД
# DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
# engine = create_async_engine(DATABASE_URL)
# async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
DB_SERVICE_URL = "http://localhost:8000"

async def get_http_session() -> AsyncGenerator:
    """
    Получение сессии БД

    :return: AsyncGenerator[AsyncSession, None]
    """
    # async with async_session_maker() as session:
    #     yield session
    async with ClientSession(base_url=DB_SERVICE_URL) as session:
        yield session
