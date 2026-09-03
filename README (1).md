# fx-buddy 환율 데이터 Firestore 업로드 가이드

## 1. 폴더 준비
컴퓨터에 새 폴더를 하나 만들고, 아래 3개 파일을 그 안에 넣어주세요.

- `upload_to_firestore.py` (업로드 스크립트)
- `환율_data.csv` (895개 환율 데이터)
- `fx-buddy-firebase-adminsdk-fbsvc-e38e7b3920.json` (Firebase에서 다운받은 서비스 계정 키 — 다운로드 폴더에 있을 거예요, 여기로 옮겨서 같이 넣어주세요)

## 2. 가상환경 만들기 (터미널/명령 프롬프트에서)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

## 3. 패키지 설치

```bash
pip install firebase-admin
```

## 4. 실행

```bash
python upload_to_firestore.py
```

정상적으로 실행되면 이런 메시지가 순서대로 뜰 거예요.

```
총 895개 레코드를 읽었어요. Firestore에 업로드를 시작합니다...
  ...500/895개 업로드 완료
  ...895/895개 업로드 완료
전체 업로드가 끝났어요! Firebase 콘솔의 Firestore Database에서 'data' 컬렉션을 확인해보세요.
```

## 5. 확인

Firebase 콘솔 → fx-buddy 프로젝트 → Firestore Database → `data` 컬렉션을 열어서
문서 895개가 들어있는지, 필드(date, value, memo)가 잘 보이는지 확인하세요.

## ⚠️ 보안 주의

- JSON 키 파일은 **GitHub에 절대 올리지 마세요**.
- 나중에 이 프로젝트를 GitHub에 올릴 때는, `.gitignore` 파일에 아래 줄을 추가하세요.

```
*.json
venv/
.env
```

(단, 나중에 다른 설정용 json이 필요해지면 이 규칙을 세밀하게 조정하세요.)
