FastAPI + Whisper + OpenAI API 기반 `ai-curriculum-analysis-server` 기준으로 작성했습니다.

---

## ✅ README.md 템플릿

```markdown
# AI Curriculum Analysis Server

이 프로젝트는 업로드된 강의 영상에서 음성을 추출하고, Whisper로 텍스트로 변환한 뒤 OpenAI GPT API를 통해 초보자 맞춤 커리큘럼을 자동 생성하는 FastAPI 기반 백엔드 서버입니다.

---

## 🛠️ 기술 스택

- Python 3.11
- FastAPI
- Whisper (OpenAI 음성 인식)
- OpenAI GPT-3.5/4 API
- ffmpeg (오디오 추출용)
- Uvicorn (ASGI 서버)
- dotenv (.env 환경변수 설정)

---

## 📦 설치 및 실행 방법

### 1. 리포지토리 클론

```bash
git clone https://github.com/Team-Study-Bridge/ai-curriculum-analysis-server.git
cd ai-curriculum-analysis-server
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. `.env` 파일 생성

```bash
cp .env.example .env
```

그리고 다음과 같이 환경변수를 설정합니다:

```env
OPENAI_API_KEY=sk-xxx... (OpenAI API 키 입력)
```

### 5. ffmpeg 설치

- [ffmpeg 공식 다운로드](https://ffmpeg.org/download.html)에서 설치 후, 환경변수에 `ffmpeg` 경로를 추가합니다.
- 또는 Windows에서는 Chocolatey 사용:
```bash
choco install ffmpeg
```

### 6. 서버 실행

```bash
uvicorn main:app --reload
```

접속 URL: [http://localhost:8000](http://localhost:8000)

---

## 📤 API 사용 방법

### POST `/api/ai/generate-curriculum`

- 업로드된 `.mp4` 영상에서 커리큘럼을 자동 생성합니다.
- 요청 형식: `multipart/form-data`
- 파라미터:
  - `videoFile`: 영상 파일 (예: 강의.mp4)

#### 응답 예시

```json
{
  "transcript": "이 강의는 ...",
  "curriculum": "- 1단계: 변수의 개념\n- 2단계: 조건문 사용법..."
}
```

---

## 📝 주의사항

- Whisper 모델 로딩 속도가 느릴 수 있으니 최초 호출 시 다소 시간이 소요됩니다.
- GPT 호출 시 OpenAI API 키가 유효해야 합니다.

---

## 📁 폴더 구조

```bash
ai-curriculum-analysis-server/
├── app/                # 주요 모듈
├── main.py             # FastAPI 엔트리포인트
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 📄 라이선스

MIT License
```

---

### ✅ 추가 파일: `.env.example`

```env
# .env.example
OPENAI_API_KEY=your_openai_api_key_here
