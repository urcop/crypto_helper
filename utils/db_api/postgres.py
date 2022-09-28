import contextlib
from typing import Optional, AsyncIterator

import asyncpg
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self._pool: Optional[Pool] = None

    async def create_table_users(self):
        sql = '''
             create table if not exists users (
                 id serial primary key,
                 fullname varchar(255) not null,
                 username varchar(255) null,
                 tg_id bigint not null unique,
                 is_admin bool not null default false,
                 balance real not null default 0.0,
                 refer_id int not null default 0,
                 api_key varchar(255) not null default '-',
                 secret_key varchar(255) not null default '-',
                 lang varchar(2) not null default 'ru'
             );
         '''
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, tg_id, username, fullname, refer_id, lang):
        sql = """
            insert into users(fullname, username, tg_id, refer_id, lang) VALUES ($1, $2, $3, $4, $5) returning *
        """
        return await self.execute(sql, fullname, username, tg_id, refer_id, lang, fetchrow=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def get_balance(self, tg_id):
        sql = """
            select balance from users where tg_id=$1
        """
        return await self.execute(sql, tg_id, fetchval=True)

    async def get_earn(self, tg_id):
        sql = """
            select earn from users where tg_id=$1
        """
        return await self.execute(sql, tg_id, fetchval=True)

    async def balance(self, tg_id, count, give=False, take=False, earn=False):
        sql = ''
        if give:
            sql = """
                update users set balance = balance + $1 where tg_id=$2
            """
        elif take:
            sql = """
                update users set balance = balance - $1 where tg_id=$2
            """
        elif earn:
            sql = """
                update users set earn = earn + $1 where tg_id=$2
            """
        return await self.execute(sql, count, tg_id, execute=True)

    async def view_5_lvl(self, tg_id):
        sql = """
            select lev1.refer_id, lev2.refer_id, lev3.refer_id, lev4.refer_id, lev5.refer_id
                from  users lev1
                left join users lev2 on (lev2.tg_id = lev1.refer_id)
                left join users lev3 on (lev3.tg_id = lev2.refer_id)
                left join users lev4 on (lev4.tg_id = lev3.refer_id)
                left join users lev5 on (lev5.tg_id = lev4.refer_id)
                where lev1.tg_id = $1;
        """
        return await self.execute(sql, tg_id, fetchrow=True)

    async def count_refs(self, tg_id):
        sql = """
            select  count(DISTINCT lev1.tg_id), count(DISTINCT lev2.tg_id), count(DISTINCT lev3.tg_id), count(DISTINCT lev4.tg_id), count(DISTINCT lev5.tg_id)
                from  users lev1
                left join users lev2 on (lev2.refer_id = lev1.tg_id)
                left join users lev3 on (lev3.refer_id = lev2.tg_id)
                left join users lev4 on (lev4.refer_id = lev3.tg_id)
                left join users lev5 on (lev5.refer_id = lev4.tg_id)
                where lev1.refer_id = $1;
        """
        return await self.execute(sql, tg_id, fetchrow=True)

    async def language(self, tg_id, lang='ru', update=False, take=False):
        if update:
            sql = """
                update users set lang=$2 where tg_id=$1
            """
            return await self.execute(sql, tg_id, lang, execute=True)
        elif take:
            sql = """
                select lang from users where tg_id=$1
            """
            return await self.execute(sql, tg_id, fetchval=True)

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self._transaction() as connection:
            if fetch:
                result = await connection.fetch(command, *args)
            elif fetchval:
                result = await connection.fetchval(command, *args)
            elif fetchrow:
                result = await connection.fetchrow(command, *args)
            elif execute:
                result = await connection.execute(command, *args)
        return result

    @contextlib.asynccontextmanager
    async def _transaction(self) -> AsyncIterator[asyncpg.Connection]:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASS,
                host=config.DB_HOST,
                database=config.DB_NAME,
                port=config.DB_PORT
            )
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                yield conn

    async def close(self) -> None:
        if self._pool is None:
            return None

        await self._pool.close()


if __name__ == "__main__":
    pass
