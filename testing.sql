CREATE TABLE user (
userid INTEGER PRIMARY KEY,
username varchar(20) NOT NULL,
password varchar(50) NOT NULL,
firstname varchar(100),
lastname varchar(100),
salt varchar(10)
);
