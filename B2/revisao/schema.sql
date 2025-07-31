drop table if exists users;

create table users (
    id integer primary key autoincrement,
    nome text not null
);