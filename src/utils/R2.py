import aioboto3
from settings import settings

class R2Storage:
    def __init__(self):
        # Сессию можно создать один раз
        self.session = aioboto3.Session()

    async def upload_file(self, file, object_name):
        endpoint = settings.R2_ENDPOINT_URL
        access_key = settings.R2_ACCESS_KEY_ID
        secret_key = settings.R2_SECRET_ACCESS_KEY
        bucket = settings.R2_BUCKET_NAME

        if not all([endpoint, access_key, secret_key, bucket]):
            raise ValueError(f"Ошибка: Не все ключи R2 найдены! Endpoint: {endpoint} {__name__}")

        async with self.session.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name="auto",
        ) as s3:
            file_content = await file.read()
            await s3.put_object(
                Bucket=bucket,
                Key=object_name,
                Body=file_content,
                ContentType=file.content_type
            )
            return f"{settings.R2_PUBLIC_URL}/{object_name}"

storage = R2Storage()