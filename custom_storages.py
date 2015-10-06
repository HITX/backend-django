from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

class StaticStorage(S3BotoStorage):
    bucket_name = settings.AWS_STORAGE_STATIC_BUCKET_NAME

class MediaStorage(S3BotoStorage):
    bucket_name = settings.AWS_STORAGE_MEDIA_BUCKET_NAME

class PrivateMediaStorage(MediaStorage):
    default_acl = 'private'
    querystring_auth = True
    querystring_expire = 600
