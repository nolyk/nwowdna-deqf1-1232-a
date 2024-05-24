from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "username" VARCHAR(50),
    "status" VARCHAR(20) NOT NULL,
    "balance" REAL NOT NULL  DEFAULT 0,
    "rating" BIGINT NOT NULL  DEFAULT 0,
    "deals" BIGINT NOT NULL  DEFAULT 0,
    "who_invite" BIGINT NOT NULL  DEFAULT 0,
    "date" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "ban" INT NOT NULL  DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
