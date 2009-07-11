CREATE TABLE user (
userid int NOT NULL PRIMARY KEY,
username varchar(20) NOT NULL,
pasword varchar(50) NOT NULL,
firstname varchar(100),
lastname varchar(100)
);

INSERT INTO user VALUES (1, 'admin', 'aaa', 'Admin', 'User');
INSERT INTO user VALUES (2, 'test1', 'bbb', 'Joe', 'Smith');
INSERT INTO user VALUES (3, 'test2', 'ccc', 'Bob', 'King');