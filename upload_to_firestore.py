"""
fx-buddy 프로젝트: 환율 데이터를 Firestore 'data' 컬렉션에 업로드하는 스크립트

사용법:
1. 이 파일과 같은 폴더에 서비스 계정 키 JSON 파일을 두세요.
   (예: fx-buddy-firebase-adminsdk-fbsvc-e38e7b3920.json)
2. 아래 SERVICE_ACCOUNT_KEY_PATH 를 실제 파일명으로 맞춰주세요.
3. 터미널에서 실행:
   pip install firebase-admin
   python upload_to_firestore.py
"""

import csv
import os
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore

# ---------------------------------------------------------
# 1. 설정값 (본인 환경에 맞게 수정)
# ---------------------------------------------------------
SERVICE_ACCOUNT_KEY_PATH = "fx-buddy-firebase-adminsdk-fbsvc-e38e7b3920.json"
CSV_PATH = "환율_data.csv"
COLLECTION_NAME = "data"

# ---------------------------------------------------------
# 2. Firebase 초기화
# ---------------------------------------------------------
if not os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
    raise FileNotFoundError(
        f"서비스 계정 키 파일을 찾을 수 없어요: {SERVICE_ACCOUNT_KEY_PATH}\n"
        "이 스크립트와 같은 폴더에 JSON 키 파일을 넣었는지 확인해주세요."
    )

cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------------------------------------------------------
# 3. CSV 읽기
# ---------------------------------------------------------
records = []
with open(CSV_PATH, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        records.append({
            "date": row["date"],
            "value": float(row["value"]),
            "memo": row["memo"],
        })

print(f"총 {len(records)}개 레코드를 읽었어요. Firestore에 업로드를 시작합니다...")

# ---------------------------------------------------------
# 4. Firestore batch write (500개씩 나눠서 업로드)
# ---------------------------------------------------------
BATCH_LIMIT = 500
count = 0

for i in range(0, len(records), BATCH_LIMIT):
    batch = db.batch()
    chunk = records[i:i + BATCH_LIMIT]

    for rec in chunk:
        # 문서 ID를 날짜로 지정 -> 같은 날짜 데이터가 중복 업로드되지 않고 덮어써짐
        doc_ref = db.collection(COLLECTION_NAME).document(rec["date"])
        batch.set(doc_ref, {
            "date": rec["date"],
            "value": rec["value"],
            "memo": rec["memo"],
            "created_at": firestore.SERVER_TIMESTAMP,
        })

    batch.commit()
    count += len(chunk)
    print(f"  ...{count}/{len(records)}개 업로드 완료")

print("전체 업로드가 끝났어요! Firebase 콘솔의 Firestore Database에서 'data' 컬렉션을 확인해보세요.")
