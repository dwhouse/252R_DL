#!/bin/bash

# Homebrew 환경 변수 설정을 스크립트에 추가
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

# 터미널에서 실행

# * HOW TO *
# 1. 실행 전 권한 부여
# chmod +x make_sample_sqldb.sh
# 2. 스크립트 실행
# ./make_sample_sqldb.sh

# 1. HomeBrew로 MySQL 설치
echo "Installing MySQL via HomeBrew..."
brew list mysql &>/dev/null || brew install mysql

# 2. MySQL 서비스 시작
echo "Starting MySQL service..."
brew services list | grep mysql | grep started &>/dev/null || brew services start mysql

# 3. MySQL에 접속하여 데이터베이스 및 테이블 생성, 데이터 삽입
echo "Setting up sample database and table..."

mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS test_db;
USE test_db;
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    email VARCHAR(100),
    age INT
);
INSERT INTO users (id, name, email, age) VALUES
(1, 'Alice', 'alice@example.com', 30),
(2, 'Bob', 'bob@example.com', 25),
(3, 'Charlie', 'charlie@example.com', 35);
EOF

echo "Sample database and table setup completed."