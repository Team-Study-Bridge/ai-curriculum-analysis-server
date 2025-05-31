FROM python:3.11-slim

# 1. 가상환경 디렉토리 설정 및 생성
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV

# 2. venv 환경이 기본 PATH로 잡히도록 설정
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

# 3. 필요한 시스템 패키지 설치 (git 등)
RUN apt-get update && apt-get install -y git

# 4. requirements.txt 복사 후 패키지 설치 (venv 활성화 상태)
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 5. 소스 복사
COPY . .

# 6. 앱 실행 (uvicorn도 requirements.txt에 명시!)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
