# 🗣️ VOICE ChatBOT 실습
### 🌿부야오 샹차이!
- 세계 최대 영어 능력 평가 지수 EF EPI에 따르면, 중국은 EF EPI 점수가 464점으로, 글로벌 평균 점수보다 낮음
  <img width="623" height="322" alt="비교" src="https://github.com/user-attachments/assets/5e6632e8-297b-4815-a474-2ce396cbfbb4" />

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
<img width="80%" height="80%" alt="voice_chatbot_1" src="https://github.com/user-attachments/assets/c3f4e4d5-213f-484b-8279-e3c8602d22b4" />

- 음성 입력 시 (한국어 입력/중국어 입력)
<img width="782" height="667" alt="voice_chatbot_2" src="https://github.com/user-attachments/assets/b62b1747-bb77-47c9-9a93-fdc9aad6835f" />

- 욕설 감지 시
<img width="755" height="433" alt="voice_chatbot_3" src="https://github.com/user-attachments/assets/62604a79-957b-4248-8266-00942c19fbc5" />

---

### 코멘트
- `main_page.py`의 디자인은 Claude를 활용했습니다.
- 디자인이 들어가지 않은 원본 코드는 code에서 확인 가능합니다.
