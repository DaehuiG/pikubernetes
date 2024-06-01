# 베이스 이미지로 Python 3.9 사용
FROM python:3.9

# 작업 디렉토리를 설정
WORKDIR /app

# 필요한 패키지 목록 불러오기
COPY requirements.txt .

# 패키지를 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드를 복사
COPY . .

# Streamlit 설정 파일 생성
RUN mkdir -p ~/.streamlit && \
    echo "[server]\nheadless = true\nport = 80\nenableCORS = false\n\n" > ~/.streamlit/config.toml

# 컨테이너 시작 시 Streamlit 앱을 실행
CMD ["streamlit", "run", "front.py"]