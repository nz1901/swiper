import random
import json

from django.core.cache import cache
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from django.conf import settings

from swiper import config
from common import keys
from worker import celery_app

def gen_vcode(size=4):
    # 返回4位随机数 ( 1000, 9999)
    start = 10 ** (size - 1)
    end = 10 ** size - 1
    return str(random.randint(start, end))
#
#
# def send_sms(phone):
#     data = config.YZX_PARAMS.copy()
#     vcode = gen_vcode()
#     # 把vcode存入缓存中
#     # VCODE-186766896715
#     key = keys % phone
#     cache.set(key, vcode, timeout=180)
#     data['param'] = vcode
#     data['mobile'] = phone
#     response = requests.post(config.YZX_URL, json=data)
#     if response.status_code != 200:
#         return False
#     return True

client = AcsClient(config.AK_ID, config.AK_SE, 'cn-hangzhou')


@celery_app.task
def send_sms(phone):
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', "18676689715")
    request.add_query_param('SignName', "swiper")
    request.add_query_param('TemplateCode', "SMS_189840981")
    vcode = gen_vcode()
    print('vcode:', vcode)
    code_dict = {
        'code': vcode
    }
    # 把code加入缓存
    key = keys.VCODE % phone
    # 优化: 开发环境, 验证码缓存14天, 正式环境缓存15分钟
    timeout = 86400 if settings.DEBUG else 900
    cache.set(key, vcode, timeout=timeout)
    request.add_query_param('TemplateParam', json.dumps(code_dict))
    response = client.do_action_with_exception(request)
    result = json.loads(response, encoding='utf-8')
    code = result.get('Code')
    if code == 'OK':
        return True
    return False
