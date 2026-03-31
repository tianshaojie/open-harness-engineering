import asyncio
import hashlib
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/open_harness_engineering"

async def fix_password():
    # 计算正确的密码哈希
    password = "Admin@123"
    hashed = hashlib.sha256(password.encode()).hexdigest()
    print(f"正确的密码哈希: {hashed}")
    
    # 连接数据库
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # 查询当前密码
        result = await session.execute(
            text("SELECT id, username, password FROM sys_user WHERE username='superadmin'")
        )
        user = result.fetchone()
        if user:
            print(f"\n当前用户: {user}")
            print(f"当前密码哈希: {user[2]}")
            
            # 更新密码
            await session.execute(
                text("UPDATE sys_user SET password=:pwd WHERE username='superadmin'"),
                {"pwd": hashed}
            )
            await session.commit()
            print(f"\n✅ 密码已更新为: {hashed}")
        else:
            print("❌ 未找到superadmin用户")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(fix_password())
