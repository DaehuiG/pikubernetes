# Base 이미지
FROM python:3.12-slim

RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN echo Asia/Seoul > /etc/timezone

# 2. 작업 디렉토리를 /app으로 설정
WORKDIR /code
# 3. 현재 디렉토리의 requirements.txt 파일을 컨테이너의 /app으로 복사
COPY requirements.txt /app/
COPY . .

# 4. requirements.txt에 명시된 패키지 설치
RUN apt-get update
RUN apt-get upgrade -y
RUN pip3 install -r requirements.txt

#8. 실행될 컨테이너 구성
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]