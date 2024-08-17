import random

from dotenv import load_dotenv, dotenv_values
from kavenegar import *
from django.conf import settings


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
    min_num = int(f"1{'0' * (settings.OTP_LENGTH - 1)}")
    max_num = int(f"9{'9' * (settings.OTP_LENGTH - 1)}")
    return str(random.randint(min_num, max_num))
