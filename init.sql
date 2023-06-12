CREATE TABLE chats
(
    id        SERIAL PRIMARY KEY,
    chat_id   BIGINT UNIQUE,
    username VARCHAR(500)
);