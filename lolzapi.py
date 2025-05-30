import time
import random
import secrets
import json
import requests

start_time = int(time.time())

def check_payment(date):
    if date >= start_time:
        return True
    else:
        return False


class Lolz():
    def __init__(self, access_token: str):
        self.api_url = 'https://api.zelenka.guru/'

        self.session = requests.session()
        self.session.headers = {
            'Authorization': f'Bearer {access_token}'
            }
        self.user = self.get_user()
        self.user_id = self.user['user_id']
        self.username = self.user['username']

    def get_user(self):
        response = self.session.get('https://api.lzt.market/me')
        if response.status_code == 200:
            response = response.json()
            if 'user' not in response.keys():
                raise ValueError('Invalid Token')
            return response['user']
        else:
            print(response.json())
            raise BaseException(response.text.split('<h1>')[1].split('</h1>')[0])

    def get_link(self, amount: int, comment: str):
        return f'https://lzt.market/balance/transfer?username={self.username}&hold=0&amount={amount}&comment={comment}'

    def get_random_string(self):
        return f'{time.time()}_{secrets.token_hex(random.randint(12, 20))}'

    def check_payment(self, amount: int, comment: str):
        data = {
            "type" : "money_transfer",
            "is_hold" : 0
        }
        response = self.session.get(f'{self.api_url}market/user/{self.user_id}/payments')
        if response.status_code == 200:
            payments = response.json()['payments']
            for payment in payments.values():
                if 'Перевод денег от' in payment['label']['title'] and int(amount) == payment['incoming_sum'] and comment == payment['data']['comment']:
                    return True
            return False
        else:
            raise BaseException(response.text.split('<h1>')[1].split('</h1>')[0])

    def get_payments(self):
        data = {
            "type": "money_transfer",
            "is_hold": 0
        }
        response = self.session.get(f'{self.api_url}market/user/{self.user_id}/payments')
        if response.status_code == 200:
            payments = response.json().get('payments', {})
            donations = []
            for payment in payments.values():
                if 'Перевод денег от' in payment['label']['title']:
                    comment = payment["data"].get("comment", "")
                    nick = payment["data"].get("username", "")
                    amount = payment["incoming_sum"]
                    date = payment["operation_date"]
                    oid = payment["operation_id"]
                    res = check_payment(date)
                    if not res:
                        continue
              
                    try:
                        number = float(amount)
                        if number >= 2:
                            donations.append({
                                "comment": comment,
                                "username": nick,
                                "amount": amount,
                                "date": date,
                                "operation_id": oid
                            })
                    except:
                        print("ошибка епта")
         
            
            return json.dumps({"donats": donations}, ensure_ascii=False)
        else:
            raise BaseException(response.text.split('<h1>')[1].split('</h1>')[0])