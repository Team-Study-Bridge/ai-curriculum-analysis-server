FROM python:3.11-slim

# NumPy 호환성을 위한 환경변수 설정
ENV NPY_NUM_BUILD_JOBS=1
ENV PYTHONUNBUFFERED=1

# 가상환경 디렉토리 설정 및 생성
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV

# venv 환경이 기본 PATH로 잡히도록 설정
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

# 필요한 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사 후 패키지 설치
COPY requirements.txt ./

# pip 업그레이드 및 NumPy 먼저 설치
RUN pip install --upgrade pip setuptools wheel \
    && pip install "numpy<2.0.0" \
    && pip install --no-cache-dir -r requirements.txt

# 소스 복사
COPY . .

# 앱 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]