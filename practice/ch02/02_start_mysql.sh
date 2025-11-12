#!/bin/bash

# --- Homebrew 환경 설정 ---
# 스크립트 환경에서 'brew' 명령어를 찾을 수 있도록 경로를 설정
# Homebrew 설치 경로가 다르면 이 부분을 수정해야,,,
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

echo "Attempting to start MySQL service via Homebrew..."

# --- MySQL 서비스 시작 ---
# 'brew services list'로 현재 mysql 서비스 상태를 확인
# 'grep started'로 'started' 상태인지 확인
# '&>/dev/null'은 확인 과정의 출력 메시지를 숨김
# '||' (OR) : 만약 'started' 상태가 아니라면(grep이 실패하면) 뒤의 명령을 실행
brew services list | grep mysql | grep started &>/dev/null || brew services start mysql

# 서비스 시작 후 상태 확인
echo "Current MySQL service status:"
brew services list | grep mysql