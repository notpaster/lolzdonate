import requests
import random
import json
import time
import asyncio
from lolzapi import Lolz

token = "" # DonationAlerts Token
lzt = Lolz('') # LolzTeam Token

print("✅ Lolz Api подключен!")
print("✅ Donation Alerts Api подключен!")

payments = []
checked = []

def send_donat(name, amount, message):
    if message == "":
        message = "."
    data = {
        "id": 1,
        "name": "lolzteam",
        "external_id": "lolzid" + str(random.randint(100,100000)),
        "message": message,
        "currency": "RUB",
        "bought_amount": 2,
        "is_shown": 0,
        "header": f"{name} - {amount} RUB",
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    r = requests.post(
        "https://www.donationalerts.com/api/v1/custom_alert",
        headers=headers,
        data=json.dumps(data)
    )

    if r.status_code == 201:
        print("✅ Донат успешно обработан!")
    else:
        print(r.text)
        print("❌ Донат не обработан")

async def fetch_payments(payments):
    while True:
        try:
            raw_data = lzt.get_payments()
        except:
            time.sleep(5)
            raw_data = lzt.get_payments()
        try:
            data = json.loads(raw_data)

            if "donats" in data and data["donats"]:
                for donat in data["donats"]:
                    if donat not in checked:
                        payments.append(donat)
                        checked.append(donat)
        except json.JSONDecodeError:
            print("Ошибка: Получены некорректные данные:", raw_data)
        except Exception as e:
            print("Ошибка:", e)

        await asyncio.sleep(5)

async def process_payments(payments):
    while True:
        for donat in payments:
            send_donat(donat["username"], donat["amount"].replace(".00", ""), donat["comment"])
            print("💲 Запрос на донат отправлен!")
            payments.remove(donat)
            continue
        await asyncio.sleep(10)

async def main():
    payments = []
    await asyncio.gather(
        fetch_payments(payments),
        process_payments(payments)
    )

print("🔎 Ищу новые донаты...")
asyncio.run(main())