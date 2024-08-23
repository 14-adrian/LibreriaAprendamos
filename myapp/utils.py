import boto3
from django.conf import settings
from botocore.exceptions import NoCredentialsError

def subir_archivo_s3(archivo, nombre_archivo):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    
    try:
        s3.upload_fileobj(archivo, settings.AWS_STORAGE_BUCKET_NAME, nombre_archivo)
        url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{nombre_archivo}"
        return url  # Devuelve la URL del archivo subido
    except NoCredentialsError:
        print("Credenciales no encontradas")
        return None