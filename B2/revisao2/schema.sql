drop table if exists jogo;

create table jogo (
    id integer primary key autoincrement,
    nomepersonagem text not null,
    jogoorigem text not null,
    habilidade text not null
);
