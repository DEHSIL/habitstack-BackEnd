from fastapi.middleware.cors import CORSMiddleware
from src.web import user, auth
from contextlib import asynccontextmanager
from src.utils.db import engine, Base
from fastapi import FastAPI

from src.web import user_admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(
    lifespan=lifespan,
    response_model_exclude_none=True
)
origins = [
    "http://localhost:3000",  # Твой фронтенд на Next.js
    "http://127.0.0.1:3000",  # На всякий случай локальный IP
]

# Добавляем CORSMiddleware в приложение
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Разрешаем запросы с этих адресов
    allow_credentials=True,           # Разрешаем передачу кук и заголовков авторизации
    allow_methods=["*"],              # Разрешаем все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],              # Разрешаем любые HTTP-заголовки
)

app.include_router(user.router)
app.include_router(user_admin.router)
app.include_router(auth.router)