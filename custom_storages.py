from django.conf import settings
from django.utils.deconstruct import deconstructible
from storages.backends.s3boto import S3BotoStorage

@deconstructible
class StaticStorage(S3BotoStorage):
    bucket_name = settings.AWS_STORAGE_STATIC_BUCKET_NAME

@deconstructible
class MediaStorage(S3BotoStorage):
    bucket_name = settings.AWS_STORAGE_MEDIA_BUCKET_NAME

@deconstructible
class PrivateMediaStorage(MediaStorage):
    default_acl = 'private'
    querystring_auth = True
    querystring_expire = 600
