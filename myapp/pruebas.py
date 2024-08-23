import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def verificar_conexion_s3():
    
    try:
        # Crear cliente S3
        s3 = boto3.client('s3')
        
        # Listar los buckets
        response = s3.list_buckets()
        print("Conexión exitosa. Buckets disponibles:")
        for bucket in response['Buckets']:
            print(f'- {bucket["Name"]}')
            
    except NoCredentialsError:
        print("No se encontraron credenciales. Verifica tus claves de acceso.")
    except PartialCredentialsError:
        print("Las credenciales proporcionadas son parciales o incorrectas.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

    

# Llamar a la función para verificar la conexión
verificar_conexion_s3()
