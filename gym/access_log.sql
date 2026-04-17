CREATE TABLE access_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    학번 VARCHAR(100),
    이름 VARCHAR(100),
    구분 VARCHAR(50),
    입실일자 VARCHAR(10),
    입실시간 VARCHAR(8),
    퇴실일자 VARCHAR(10) DEFAULT '',
    퇴실시간 VARCHAR(8) DEFAULT '',
    이용구분 VARCHAR(50) DEFAULT '',
    비고 VARCHAR(255) DEFAULT ''
);