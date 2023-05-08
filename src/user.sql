DROP TABLE IF EXISTS account;

CREATE TABLE IF NOT EXISTS account (
    userid text,
    password text,
    email text
);

DROP TABLE IF EXISTS friend;

CREATE TABLE IF NOT EXISTS friend (
    userid text,
    friendid text
);


INSERT INTO account VAlUES ('huyhoang', '123456', 'huy@gmail.com');
INSERT INTO account VAlUES ('danh', '123789', 'danh@gmail.com');
INSERT INTO account VAlUES ('huy', '123', 'huy@gmail.com');
INSERT INTO friend VAlUES ('huyhoang', 'danh');
INSERT INTO friend VAlUES ('danh', 'huyhoang');
