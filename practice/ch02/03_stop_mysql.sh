#!/bin/bash

# --- Homebrew 환경 설정 ---
# 스크립트 환경에서 'brew' 명령어를 찾을 수 있도록 경로를 설정
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

echo "Attempting to stop MySQL service via Homebrew..."

# --- MySQL 서비스 중지 ---
# 'brew services list'로 현재 mysql 서비스 상태를 확인
# 'grep started'로 'started' 상태인지 확인
# '&>/dev/null'은 확인 과정의 출력 메시지를 숨김
# '&&' (AND) : 만약 'started' 상태가 맞다면(grep이 성공하면) 뒤의 명령을 실행
brew services list | grep mysql | grep started &>/dev/null && brew services stop mysql

# 서비스 중지 후 상태 확인
echo "Current MySQL service status:"
brew services list | grep mysql