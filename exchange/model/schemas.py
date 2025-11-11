from pydantic import BaseModel, BaseSettings, validator, root_validator
from typing import Literal, Union, Optional
import os
from pathlib import Path
from enum import Enum
from devtools import debug

CRYPTO_LITERAL = Literal["BINANCE", "UPBIT", "BYBIT", "BITGET", "OKX"]


STOCK_LITERAL = Literal[
    "KRX",
    "NASDAQ",
    "NYSE",
    "AMEX",
]


EXCHANGE_LITERAL = Literal[
    "BINANCE",
    "UPBIT",
    "BYBIT",
    "BITGET",
    "OKX",
    "KRX",
    "NASDAQ",
    "NYSE",
    "AMEX",
]

QUOTE_LITERAL = Literal[
    "USDT", "USDT.P", "USDTPERP", "BUSD", "BUSD.P", "BUSDPERP", "KRW", "USD", "USD.P"
]

SIDE_LITERAL = Literal[
    "buy", "sell", "entry/buy", "entry/sell", "close/buy", "close/sell"
]


def find_env_file():
    current_path = os.path.abspath(__file__)
    while True:
        parent_path = os.path.dirname(current_path)
        env_path = os.path.join(parent_path, ".env")
        dev_env_path = os.path.join(parent_path, ".env.dev")
        if os.path.isfile(dev_env_path):
            return dev_env_path
        elif os.path.isfile(env_path):
            return env_path
        if parent_path == current_path:
            break
        current_path = parent_path
    return None


env_path = find_env_file()


CRYPTO_EXCHANGES = ("BINANCE", "UPBIT", "BYBIT", "BITGET", "OKX")

STOCK_EXCHANGES = (
    "KRX",
    "NASDAQ",
    "NYSE",
    "AMEX",
)

COST_BASED_ORDER_EXCHANGES = ("UPBIT", "BYBIT", "BITGET")

NO_ORDER_AMOUNT_OUTPUT_EXCHANGES = (
    "BITGET",
    "KRX",
    "NASDAQ",
    "NYSE",
    "AMEX",
)

# "BITGET", "KRX", "NASDAQ", "AMEX", "NYSE")


crypto_futures_code = ("PERP", ".P")

# Literal[
#     "KRW", "USDT", "USDTPERP", "BUSD", "BUSDPERP", "USDT.P", "USD", "BUSD.P"
# ]


class Settings(BaseSettings):
    PASSWORD: str
    WHITELIST: Optional[list[str]] = None
    PORT: Optional[int] = None
    DISCORD_WEBHOOK_URL: Optional[str] = None
    UPBIT_KEY: Optional[str] = None
    UPBIT_SECRET: Optional[str] = None
    BINANCE_KEY: Optional[str] = None
    BINANCE_SECRET: Optional[str] = None
    BYBIT_KEY: Optional[str] = None
    BYBIT_SECRET: Optional[str] = None
    BITGET_KEY: Optional[str] = None
    BITGET_SECRET: Optional[str] = None
    BITGET_PASSPHRASE: Optional[str] = None
    OKX_KEY: Optional[str] = None
    OKX_SECRET: Optional[str] = None
    OKX_PASSPHRASE: Optional[str] = None
    OKX_SANDBOX_MODE: bool = False
    KIS1_ACCOUNT_NUMBER: Optional[str] = None
    KIS1_ACCOUNT_CODE: Optional[str] = None
    KIS1_KEY: Optional[str] = None
    KIS1_SECRET: Optional[str] = None
    KIS2_ACCOUNT_NUMBER: Optional[str] = None
    KIS2_ACCOUNT_CODE: Optional[str] = None
    KIS2_KEY: Optional[str] = None
    KIS2_SECRET: Optional[str] = None
    KIS3_ACCOUNT_NUMBER: Optional[str] = None
    KIS3_ACCOUNT_CODE: Optional[str] = None
    KIS3_KEY: Optional[str] = None
    KIS3_SECRET: Optional[str] = None
    KIS4_ACCOUNT_NUMBER: Optional[str] = None
    KIS4_ACCOUNT_CODE: Optional[str] = None
    KIS4_KEY: Optional[str] = None
    KIS4_SECRET: Optional[str] = None
    DB_ID: str = "poa@admin.com"
    DB_PASSWORD: str = "poabot!@#$"

    class Config:
        env_file = env_path  # ".env"
        env_file_encoding = "utf-8"


def get_extra_order_info(order_info):
    extra_order_info = {
        "is_futures": None,
        "is_crypto": None,
        "is_stock": None,
        "is_spot": None,
        "is_entry": None,
        "is_close": None,
        "is_buy": None,
        "is_sell": None,
    }
    if order_info["exchange"] in CRYPTO_EXCHANGES:
        extra_order_info["is_crypto"] = True
        if any([order_info["quote"].endswith(code) for code in crypto_futures_code]):
            extra_order_info["is_futures"] = True
        else:
            extra_order_info["is_spot"] = True

    elif order_info["exchange"] in STOCK_EXCHANGES:
        extra_order_info["is_stock"] = True

    if order_info["side"] in ("entry/buy", "entry/sell"):
        extra_order_info["is_entry"] = True
        _side = order_info["side"].split("/")[-1]
        if _side == "buy":
            extra_order_info["is_buy"] = True
        elif _side == "sell":
            extra_order_info["is_sell"] = True
    elif order_info["side"] in ("close/buy", "close/sell"):
        extra_order_info["is_close"] = True
        _side = order_info["side"].split("/")[-1]
        if _side == "buy":
            extra_order_info["is_buy"] = True
        elif _side == "sell":
            extra_order_info["is_sell"] = True
    elif order_info["side"] == "buy":
        extra_order_info["is_buy"] = True
    elif order_info["side"] == "sell":
        extra_order_info["is_sell"] = True

    return extra_order_info


def parse_side(side: str):
    if side.startswith("entry/") or side.startswith("close/"):
        return side.split("/")[-1]
    else:
        return side


def parse_quote(quote: str):
    if quote.endswith(".P"):
        return quote.replace(".P", "")
    else:
        return quote


class OrderRequest(BaseModel):
    exchange: EXCHANGE_LITERAL
    base: str
    quote: QUOTE_LITERAL
    # QUOTE
    type: Literal["market", "limit"] = "market"
    side: SIDE_LITERAL
    amount: Optional[float] = None
    price: Optional[float] = None
    cost: Optional[float] = None
    percent: Optional[float] = None
    amount_by_percent: Optional[float] = None
    leverage: Optional[int] = None
    stop_price: Optional[float] = None
    profit_price: Optional[float] = None
    order_name: str = "주문"
    kis_number: Optional[int] = 1
    hedge: Optional[str] = None
    unified_symbol: Optional[str] = None
    is_crypto: Optional[bool] = None
    is_stock: Optional[bool] = None
    is_spot: Optional[bool] = None
    is_futures: Optional[bool] = None
    is_coinm: Optional[bool] = None
    is_entry: Optional[bool] = None
    is_close: Optional[bool] = None
    is_buy: Optional[bool] = None
    is_sell: Optional[bool] = None
    is_total: Optional[bool] = None
    is_contract: Optional[bool] = None
    contract_size: Optional[float] = None
    margin_mode: Optional[str] = None

    class Config:
        use_enum_values = True

    @root_validator(pre=True)
    def root_validate(cls, values):
        # "NaN" to None
        for key, value in values.items():
            if isinstance(value, str):
                values[key] = value.replace(',', '')
            if values[key] in ("NaN", ""):
                values[key] = None
            

        values |= get_extra_order_info(values)

        values["side"] = parse_side(values["side"])
        values["quote"] = parse_quote(values["quote"])
        base = values["base"]
        quote = values["quote"]
        unified_symbol = f"{base}/{quote}"
        exchange = values["exchange"]
        if values["is_futures"]:
            if quote == "USD":
                unified_symbol = f"{base}/{quote}:{base}"
                values["is_coinm"] = True
            else:
                unified_symbol = f"{base}/{quote}:{quote}"

        if not values["is_stock"]:
            values["unified_symbol"] = unified_symbol

        if values["exchange"] in STOCK_EXCHANGES:
            values["is_stock"] = True
        return values


class OrderBase(OrderRequest):
    password: str

    @validator("password")
    def password_validate(cls, v):
        setting = Settings()
        if v != setting.PASSWORD:
            raise ValueError("비밀번호가 틀렸습니다")
        return v


class MarketOrder(OrderBase):
    price: Optional[float] = None
    type: Literal["market"] = "market"


class PriceRequest(BaseModel):
    exchange: EXCHANGE_LITERAL
    base: str
    quote: QUOTE_LITERAL
    is_crypto: Optional[bool] = None
    is_stock: Optional[bool] = None
    is_futures: Optional[bool] = None

    @root_validator(pre=True)
    def root_validate(cls, values):
        # "NaN" to None
        for key, value in values.items():
            if isinstance(value, str):
                values[key] = value.replace(',', '')
            if values[key] in ("NaN", ""):
                values[key] = None

        values |= get_extra_order_info(values)

        return values


# class PositionRequest(BaseModel):
#     exchange: EXCHANGE_LITERAL
#     base: str
#     quote: QUOTE_LITERAL


class Position(BaseModel):
    exchange: EXCHANGE_LITERAL
    base: str
    quote: QUOTE_LITERAL
    side: Literal["long", "short"]
    amount: float
    entry_price: float
    roe: float


class HedgeData(BaseModel):
    password: str
    exchange: Literal["BINANCE"]
    base: str
    quote: QUOTE_LITERAL = "USDT.P"
    amount: Optional[float] = None
    leverage: Optional[int] = None
    hedge: str

    @validator("password")
    def password_validate(cls, v):
        setting = Settings()
        if v != setting.PASSWORD:
            raise ValueError("비밀번호가 틀렸습니다")
        return v

    @root_validator(pre=True)
    def root_validate(cls, values):
        for key, value in values.items():
            if key in ("exchange", "base", "quote", "hedge"):
                values[key] = value.upper()
        return values
