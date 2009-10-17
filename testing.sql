CREATE TABLE user (
userid INTEGER PRIMARY KEY,
username varchar(20) NOT NULL,
password varchar(50) NOT NULL,
firstname varchar(100),
lastname varchar(100),
salt varchar(10)
);

-- Password is 'aaa'
INSERT INTO user VALUES (1, 'admin', 'ab5OR/l8cWmIc', 'Admin', 'User');
-- Password is 'bbb'
INSERT INTO user VALUES (2, 'test1', 'abjKJAkaL5HaE', 'Joe', 'Smith');
-- Password is 'ccc'
INSERT INTO user VALUES (3, 'test2', 'abmPzTXULWrKw', 'Bob', 'King');