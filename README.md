# PoABOT - Power of Algorithm

## 트레이딩뷰에서 전달되는 웹훅을 처리하는 봇입니다.

&nbsp;

- 지원 거래소
  - 업비트 KRW(원화) 마켓
  - 바이낸스 현물/선물 USDT,BUSD 마켓
  - 바이비트 현물/선물 USDT 마켓
  - 비트겟 현물/선물 USDT 마켓
  - 한국투자증권 한국/미국 주식 마켓

&nbsp;


## 추가 작업 내용 
 - pocketbase 실행파일 추가 
 - python 3.9 환경을 위한 파라미터 변수 문법 rollback (가비아 파이썬 컨테이너 호스팅)
 - 자체 테스트를 위한 웹페이지 추가 
 - ccxt 버전 update (requirements.txt)
 - OKX Coin-M 거래 수량을 위한 계산 추가 
 - 프로세스 분석 자료 추가 

## 로컬PC 및 다른 방식의 호스팅에서 사용 절차
 - pocketbase 최신 버전 호환을 위한 작업 (기완료)
 - .env 파일에 비밀번호 및 거래소 정보 저장 (Discord)
 - pocketbase serve &    백그라운드 실행 
 - python run.py 실행 
 - http://localhost:8000/test 접속
 - 테스트 진행 
 - 셈플 메시지 
  ```{ "password":"비밀번호", "exchange":"OKX", "base":"BTC", "quote":"USD.P", "side":"entry/buy", "amount":"0.002", "price":"115106.2", "percent":"NaN", "leverage": "5", "margin_mode": "", "order_name":"롱" } ```

# <주의>

_본 프로젝트는 개인적으로 개발한 프로젝트를 오픈소스로 공유한 것으로_

_발생하는 문제에 대한 모든 책임은 본인에게 있습니다._

# Dependency

> [fastapi](https://github.com/tiangolo/fastapi) , [ccxt](https://github.com/ccxt/ccxt) , [uvicorn](https://github.com/encode/uvicorn)


----------
