from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import whisper
import os
import uuid
import subprocess
import traceback
from dotenv import load_dotenv
from openai import OpenAI

# .env 환경변수 로드
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# FastAPI 앱 생성
app = FastAPI()

# Whisper 모델 로딩
model = whisper.load_model("base")

# 업로드 디렉토리 생성
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/ai/api/generate-curriculum")
async def generate_curriculum(videoFile: UploadFile = File(...)):
    try:
        # 업로드된 비디오 파일 저장
        file_id = str(uuid.uuid4())
        video_path = os.path.join(UPLOAD_DIR, f"{file_id}.mp4")

        with open(video_path, "wb") as f:
            f.write(await videoFile.read())

        # ffmpeg로 오디오 추출
        audio_path = os.path.join(UPLOAD_DIR, f"{file_id}.wav")
        subprocess.run(
            ["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", audio_path],
            check=True
        )

        # Whisper로 텍스트 변환
        result = model.transcribe(audio_path)
        transcript = result["text"]

        # 프롬프트 작성
        prompt = f"""
다음 강의 대본을 바탕으로 학습 커리큘럼을 작성하세요.

조건:
- 항목은 3~6개로 구성
- 각 항목은 제목 + 설명 형식
- 초보자 기준으로 작성
- 항목에는 구체적인 기술/개념을 사용하고, 추상적 표현은 피할 것

강의 대본:
{transcript}

커리큘럼:
"""

        # GPT 호출
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 교육 콘텐츠를 작성하는 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        curriculum = completion.choices[0].message.content.strip()

        # JSON 형식으로 반환
        return JSONResponse(content={
            "transcript": transcript,
            "curriculum": curriculum
        })

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/")
def read_root():
    return {"message": "FastAPI 서버가 정상적으로 실행 중입니다!"}
