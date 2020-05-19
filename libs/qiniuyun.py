from qiniu import Auth, put_data

from swiper import config
from worker import celery_app
# 需要填写你的 Access Key 和 Secret Key
access_key = config.QN_AK
secret_key = config.QN_SK
# 构建鉴权对象
q = Auth(access_key, secret_key)


@celery_app.task
def upload_qiniu(avatar, upload_file_name):
    # 要上传的空间
    bucket_name = config.QN_BUCKET
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, upload_file_name, 3600)
    # 要上传文件的本地路径
    ret, info = put_data(token, upload_file_name, avatar)
    # print(info)
