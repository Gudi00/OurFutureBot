from sqlalchemy import select, update
from app.database.models import async_session, User, Message
from datetime import datetime, timedelta


async def save_user(tg_id: int, username: str, first_name: str, last_name: str):
    async with async_session() as session:
        user = await session.execute(select(User).where(User.tg_id == tg_id))
        user = user.scalar_one_or_none()

        if not user:
            new_user = User(tg_id=tg_id, username=username,
                            first_name=first_name, last_name=last_name)
            session.add(new_user)
            await session.commit()
            return 1


async def save_message(username: str, text: str):

    async with async_session() as session:
        async with session.begin():  # Use a transaction
            result = await session.execute(select(Message).where(Message.username == username))
            user = result.scalar_one_or_none()
            if not user:
                new_user = Message(username=username, text=text)
                session.add(new_user)
            else:

                stmt = (
                    update(Message)
                    .where(Message.username == username)
                    .values(timestamp=datetime.now(), text=text)  # Update timestamp and text
                )
                await session.execute(stmt)


        await session.commit()

async def get_info():
    try:
        async with async_session() as session:
            result = await session.execute(select(Message))
            prices = result.scalars().all()
            # Возврат данных в виде словаря
            return {price.username: price.timestamp for price in prices}
    except Exception as e:
        print('Error in take price')
        return {}


async def get_all_users():
    async with async_session() as session:
        result = await session.execute(select(Message))
        return result.scalars().all()

async def update_user_streaks():
    async with async_session() as session:
        result = await session.execute(select(Message))
        users = result.scalars().all()
        today = datetime.now()
        for user in users:
            async with session.begin():  # Use a transaction
                result = await session.execute(select(Message).where(Message.username == user.username))
                user = result.scalar_one_or_none()

                if user.timestamp >= today - timedelta(days=1):
                    result = await session.execute(select(Message.streak_days).where(Message.username == user.username))
                    result = result.scalar_one_or_none()
                else:
                    result = 0
                stmt = (
                    update(Message)
                    .where(Message.username == user.username)
                    .values(streak_days=result)  # Update timestamp and text
                )
                await session.execute(stmt)

            await session.commit()



