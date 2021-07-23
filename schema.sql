create table entrant
(
    id         serial primary key,
    entrant_id varchar,
    name       varchar,
    surname    varchar,
    patronymic varchar,
    birthday   varchar,
    gender     varchar,
    phone      varchar,
    mail       varchar,
    snils      varchar,
    hostel     varchar,
    is_hard    varchar
);
create table passport
(
    id           serial primary key,
    entrant_id   integer references entrant (id),
    series       varchar,
    number       varchar,
    issue_date   varchar,
    organization varchar,
    sub_code     varchar
);
create table certificate
(
    id           serial primary key,
    entrant_id   integer references entrant (id),
    series       varchar,
    number       varchar,
    issue_date   varchar,
    organization varchar
);
create table address
(
    id            serial primary key,
    entrant_id    integer references entrant (id),

    r_index       varchar,
    r_region_name varchar,
    r_area        varchar,
    r_city_area   varchar,
    r_city        varchar,
    r_street      varchar,

    f_index       varchar,
    f_region_name varchar,
    f_area        varchar,
    f_city_area   varchar,
    f_city        varchar,
    f_street      varchar,

    birthplace    varchar

);
create table application
(
    id           serial primary key,
    entrant_id   integer references entrant (id),
    date_changes varchar,
    status_name  varchar,
    uid          varchar,
    target       varchar,
    subdiv_name  varchar,
    id_edu_level varchar,
    edu_level    varchar
)

