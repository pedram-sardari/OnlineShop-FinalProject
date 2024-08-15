import random

from dotenv import load_dotenv, dotenv_values
from kavenegar import *


def send_otp(otp, phone='09190893312'):
    print('*' * 50, f'code: {otp}', '*' * 50)
    # try:
    #     api = KavenegarAPI(dotenv_values()['KAVENEGAR_API_KEY'])
    #     params = {
    #         'receptor': f'{phone}',
    #         'template': 'otp',
    #         'token': f'{otp}',
    #         'type': 'sms',  # sms vs call
    #     }
    #     response = api.verify_lookup(params)
    #     print(response)
    # except APIException as e:
    #     print(str(e))
    # except HTTPException as e:
    #     print(e)


def generate_otp():
    return str(random.randint(100000, 999999))
