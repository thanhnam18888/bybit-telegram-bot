import requests
import json
import time
import os

# Cấu hình từ biến môi trường Railway
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

from payment_mapping import payment_mapping

FAMILIAR_SELLERS = [
  "🐱‍👤 VB",
  "FrontMan",
  "💙MANGO💙",
  "Alexandr137",
  "AzazeL",
  "BT6",
  "GARIK1212",
  "MVG",
  "samosvaal",
  "kostik112_47",
  "25Fast_Work25",
  "TuzBtc",
  "Frilius",
  "NatashaMenyasha",
  "spotlightBT",
  "sunshineCypto",
  "Larik174",
  "Mediateam_S",
  "wyrmyon",
  "ya russkiy",
  "VipExchangers",
  "MarkusRAMEN",
  "kkub1k",
  "Mwew01",
  "Mwow",
  "Поплыл_белый",
  "MoneyTRNSFR",
  "poHuH",
  "KITOK",
  "Uniity",
  "adminRocket",
  "Junga",
  "MEDIArr",
  "Mediashka",
  "NUMBERONE",
  "Hayruddin ",
  "Zlak",
  "Max R.",
  "Gundersen2k",
  "Kurban-C",
  "minemachine",
  "khsv500",
  "Change_Fastt",
  "LedgerLegend",
  "V0VA",
  "Bit-Bit",
  "Aleks003",
  "Аnton251085",
  "DonaldT",
  "nechertiha",
  "🥒Mr.Pickle🥒",
  "Crypto-buhgalte",
  "Jack_MediaP2...",
  "boyhollow",
  "sergosr228",
  "solomkaxd",
  "YABLOKO",
  "Han_95",
  "murad_06",
  "YULIYA19",
  "Notlxxk",
  "Timur11",
  "ibnfulanabufula",
  "BULGARI",
  "Zorro0",
  "Puma_FMM",
  "🐋Big_Whale🐋",
  "Darrovall ",
  "knwnm",
  "Siberia_pay",
  "🛸P_P_P🎁",
  "Lets go",
  "rayil",
  "ReallyGood",
  "TeamBT",
  "🔝TopSellUSD",
  "MediaTeam_JK",
  "Kazibekov ",
  "Zybarefff",
  "Bastion",
  "YungersTAP2.0",
  "Amulet.bang",
  "VladislavSV",
  "danil007-obmen",
  "rasul100",
  "💎ILVL💎",
  "aloe Vera",
  "🍷Calvados",
  "🧙WizardEx",
  "dimabratskiy",
  "🌠SonicX ",
  "Snegurochka⛄",
  "Siroccor",
  "rocrptooo🌀",
  "alermo",
  "TradeIN",
  "bespredel_au",
  "MasterClass",
  "JolySpace_CHNG",
  "ahm_mag",
  "Gusman_btc",
  "davaSINGAPUR",
  "PIROZHOK",
  "Billigan",
  "Lim0n4ik",
  "❤️MANGO❤️",
  "LinMaster",
  "🛡️SparkEX",
  "BLAGO_SLOVI",
  "Banana1234",
  "Пушкин3",
  "SeishiroNagi",
  "blessed1920",
  "GoshaLiman",
  "Vroom-Vroom 2",
  "GUBERNATOR",
  "⚡️pitupishnick⚡️",
  "GrenadeCrypto",
  "Anisimov.Y",
  "GOOD CHANGE",
  "🪄KriptoPotter�",
  "EasySell",
  "DOBROPRAVDA",
  "Matori",
  "ggsnov",
  "Squash ",
  "Romalik",
  "el_mirz0",
  "chechen111",
  "FAST_OBMEN228",
  "Relax💀",
  "saintlaurent",
  "BeverlyVIZ",
  "odisey",
  "papik",
  "DONALD_T",
  "shkotkinyan",
  "kedrestka",
  "blagodete1",
  "Arclight",
  "RRasul",
  "lady’s_crypto",
  "✅safetransfer",
  "ALI011",
  "MERCHANT_BEST",
  "Eropjkeee",
  "BE4HoMoJloDou",
  "Cuteshark"
]

headers = {{
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
}}

def send_telegram_message(message):
    payload = {{"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}}
    try:
        requests.post(TELEGRAM_API, data=payload, timeout=10)
    except Exception as e:
        print("Lỗi gửi Telegram:", e)

def translate_payment(payment_ids):
    return ", ".join([payment_mapping.get(pid, pid) for pid in payment_ids])

def fetch_ads(page):
    url = "https://api2.bybit.com/fiat/otc/item/online"
    data = {{
        "userId": "",
        "tokenId": "USDT",
        "currencyId": "RUB",
        "payment": [],
        "side": "1",
        "size": "10",
        "page": str(page),
        "amount": "",
        "vaMaker": False,
        "bulkMaker": False,
        "canTrade": True,
        "verificationFilter": 0,
        "sortType": "TRADE_PRICE",
        "paymentPeriod": [],
        "itemRegion": 1,
    }}
    try:
        res = requests.post(url, headers=headers, json=data, timeout=10)
        if res.status_code == 200:
            return res.json().get("result", {{}}).get("items", [])
    except Exception as e:
        print("Lỗi lấy dữ liệu:", e)
    return []

seen_keys = set()


min_price = float(os.getenv("MIN_PRICE", "80.0"))
max_price = float(os.getenv("MAX_PRICE", "90.0"))

while True:
    all_ads = []
    for page in range(1, 11):
        all_ads.extend(fetch_ads(page))
        time.sleep(0.2)

    for ad in all_ads:
        nickname = ad.get("nickName")
        price = float(ad.get("price", 0))
        max_amount = ad.get("maxAmount", 0)
        min_amount = ad.get("minAmount", 0)
        if min_amount < 20000 or not (min_price <= price <= max_price):
            continue
        remark = ad.get("remark", "").strip()
        payments = translate_payment(ad.get("payments", []))
        key = f"{nickname}-{price}-{min_amount}-{max_amount}-{remark}"
        if nickname in FAMILIAR_SELLERS and key not in seen_keys:
            seen_keys.add(key)
            message = (
                f"🔔 <b>QC từ người bán quen</b>\n"
                f"<b>👤:</b> {nickname}\n"
                f"<b>💰 Giá:</b> {price:.2f} RUB\n"
                f"<b>📦 Tối đa:</b> {max_amount}\n"
                f"<b>💳:</b> {payments}\n"
                f"<b>📝:</b> {remark or 'Không có'}"
            )
            send_telegram_message(message)
    time.sleep(10)