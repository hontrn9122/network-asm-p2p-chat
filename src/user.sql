DROP TABLE IF EXISTS account;

CREATE TABLE IF NOT EXISTS account (
    user_id text,
    pwd text,
    email text
);

DROP TABLE IF EXISTS friend;

CREATE TABLE IF NOT EXISTS friend (
    user_id text,
    friend_id text
);


INSERT INTO account VAlUES ('huyhoang', '123456', 'huy@gmail.com');
INSERT INTO account VAlUES ('danh', '123789', 'danh@gmail.com');
INSERT INTO account VAlUES ('huy', '123', 'huy@gmail.com');
INSERT INTO friend VAlUES ('huyhoang', 'danh');
INSERT INTO friend VAlUES ('danh', 'huyhoang');
