```mermaid
sequenceDiagram
    participant TV as TradingView
    participant Main as FastAPI (main.py)
    participant Pex as Pexchange (pexchange.py)
    participant Bot as OKX Bot (okx.py)
    participant CCXT as CCXT Library
    participant OKX as OKX Exchange API

    Note over TV: 알림 발생 (BTC 롱 진입)
    TV->>+Main: 1. POST /order 요청 (주문 정보 JSON 전달)

    Note over Main: 2. 데이터 파싱 및 검증 (MarketOrder 모델)
    Main->>+Pex: 3. get_bot("OKX") 호출

    Pex->>+Bot: 4. Okx 클래스 인스턴스 생성
    Bot->>+CCXT: 5. ccxt.okx 초기화 (API 키 설정)
    Bot->>CCXT: 6. load_markets() 호출
    CCXT->>+OKX: 7. 마켓 정보 요청 (GET .../instruments)
    OKX-->>-CCXT: 8. 마켓 정보 응답 (수수료, 정밀도 등)
    CCXT-->>Bot: 9. 마켓 정보 캐싱 완료
    Bot-->>-Pex: 10. 초기화된 Bot 객체 반환
    Pex-->>-Main: 11. Bot 객체 반환

    Main->>Bot: 12. init_info() 호출 (주문 정보 상세 설정)
    Note over Bot: 선물/현물, 계약 사이즈 등 판단

    Main->>+Bot: 13. market_entry() 호출 (시장가 진입)
    
    Note over Bot: 14. 레버리지 설정 (5배)
    Bot->>+CCXT: set_leverage(5, ...)
    CCXT->>+OKX: 15. 레버리지 설정 요청 (POST .../set-leverage)
    OKX-->>-CCXT: 16. 레버리지 설정 완료
    CCXT-->>Bot: 
    
    Note over Bot: 17. 주문 수량 계산 (100 USD.P)
    
    Note over Bot: 18. 최종 주문 생성
    Bot->>+CCXT: create_order('BTC/USD.P:USD', 'market', 'buy', 100, ...)
    CCXT->>+OKX: 19. 주문 생성 요청 (POST .../trade/order)
    OKX-->>-CCXT: 20. 주문 체결 결과 응답
    CCXT-->>-Bot: 21. 주문 결과 반환
    Bot-->>-Main: 22. 최종 결과 반환

    Note over Main: 23. 백그라운드 작업으로 주문 결과 로깅
    Main-->>-TV: 24. {"result": "success"} 응답

```

### 그래프 단계별 설명

1.  **요청 수신 (1~2)**: `TradingView`가 `main.py`로 주문 정보를 보냅니다. `main.py`는 이 데이터를 `MarketOrder` 모델에 맞춰 파싱하고 검증합니다.
2.  **객체 생성 및 초기화 (3~11)**: `main.py`는 `pexchange.py`를 통해 `okx.py`의 `Okx` 객체를 생성합니다. 이 과정에서 `ccxt` 라이브러리가 초기화되고, `load_markets()`를 통해 `OKX Exchange API`에서 모든 거래 규격 정보를 미리 받아와 캐싱합니다.
3.  **주문 준비 (12~17)**: `main.py`는 생성된 `Okx` 객체를 이용해 주문을 준비시킵니다. `market_entry` 함수가 호출되면, 먼저 레버리지를 5배로 설정하고, 최종 주문 수량을 계산합니다.
4.  **주문 실행 및 완료 (18~24)**: `ccxt`의 `create_order` 함수를 통해 실제 주문 요청이 `OKX Exchange API`로 전송됩니다. 거래소로부터 체결 결과를 응답받으면, `main.py`는 이 성공 내역을 로그로 기록하고 `TradingView`에 최종 성공 응답을 보냅니다.