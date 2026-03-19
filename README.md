# 🗣️ VOICE ChatBOT 실습
### 🌿부야오 샹차이!
- 세계 최대 영어 능력 평가 지수 EF EPI에 따르면, 중국은 EF EPI 점수가 464점으로, 글로벌 평균 점수보다 낮음
[출처: EF 영어능력지수 등급](https://www.ef.co.kr/epi/)
- 중국 여행 시 영어가 잘 통하지 않아 곤란했던 기억이 있음

- 중화권 여행에서 사용할 수 있는 번역기를 만들고자 함
- 입력 VOICE를 프롬프트로 활용 → 영어를 모르는 상대방과도 편히 소통할 수 있게 개발

- 사용 모델: Open AI `gpt-4.1-mini`
---
### 실행
```
pip install -r requirements.txt
```
```
streamlit run main_page.py
```

---

### 예시 페이지
- 메인 페이지
<img width="785" height="732" alt="Image" src="https://github.com/user-attachments/assets/3668df0e-bca0-4732-bb6e-a87035050f22" />

- 음성 입력 시 (한국어 입력/중국어 입력)
<img width="713" height="538" alt="Image" src="https://github.com/user-attachments/assets/a424b923-f182-425b-85e6-d7982372de8d" />

- 욕설 감지 시
<img width="687" height="451" alt="Image" src="https://github.com/user-attachments/assets/adecf3da-dd70-416f-8169-0f2568b35b22" />

---

### 코멘트
- `main_page.py`의 디자인은 Claude를 활용했습니다.
- 디자인이 들어가지 않은 원본 코드는 code에서 확인 가능합니다.
