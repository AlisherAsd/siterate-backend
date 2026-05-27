from app.db import get_async_session
from sqlalchemy import select
from app.models import User
from app.users import get_user_manager, get_user_db
from app.schemas import UserCreate


async def create_superuser_if_not_exists():
    """Автоматически создает суперпользователя, если его нет"""
    async for session in get_async_session():
        result = await session.execute(
            select(User).where(User.is_superuser == True)
        )
        existing_admin = result.scalar_one_or_none()
        
        if existing_admin:
            print(f"✅ Суперпользователь уже существует: {existing_admin.email}")
            return
        
        result = await session.execute(
            select(User).where(User.email == "admin@example.com")
        )
        user = result.scalar_one_or_none()
        
        if user:
            user.is_superuser = True
            await session.commit()
            print(f"👑 Пользователь {user.email} повышен до суперпользователя")
            return
        
        print("📝 Создаем нового суперпользователя...")
        
        try:
            user_data = UserCreate(
                email="admin@example.com",
                password="string",  
                is_active=True,
                is_superuser=True,
                is_verified=True
            )
        
            async for user_db in get_user_db(session):
                async for user_manager in get_user_manager(user_db):
                    user = await user_manager.create(user_data, safe=False)
                    print(f"Суперпользователь успешно создан!")
                    print(f"Email: {user.email}")
                    print(f"Password: string")
                    print("Обязательно смените пароль после первого входа!")
                    return
                    
        except Exception as e:
            print(f"Ошибка при создании суперпользователя: {e}")
            print("Возможно, таблицы еще не созданы или пользователь уже существует")
