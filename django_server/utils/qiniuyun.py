from qiniu import Auth

access_key = 'tlFNOYPD_aAECJW7f_FKJGNV2ndaUk1-8ZvkIERD'
secret_key = 'LEaKw20aqmSqloM6jBaD4RL-2qNB7OgBicXOSL_K'

#七牛云
def qntoken():
    q = Auth(access_key, secret_key)
    # 要上传的空间   过期后需要修改
    bucket_name = 'jchservers'
    # 生成上传 Token
    token = q.upload_token(bucket_name)
    return token