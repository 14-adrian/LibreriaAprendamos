from django.db import connection
from django.conf import settings

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login

from .forms import DocumentoForm
from .models import Documento

from .utils import subir_archivo_s3


import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

Usuario = get_user_model()

@login_required
def logout_view(request):
    logout(request)  # Cierra la sesión
    return redirect('login')  # Redirige al login después de cerrar sesión

def sign_up_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre1')
        email = request.POST.get('email1')
        password = request.POST.get('password1')
        password_confirm = request.POST.get('password_confirm')

        # Validaciones básicas
        if password != password_confirm:
            error = "Las contraseñas no coinciden"
            return render(request, 'sign_up.html', {'error': error})

        if Usuario.objects.filter(email=email).exists():
            error = "El correo electrónico ya está registrado"
            return render(request, 'sign_up.html', {'error': error})

        # Crear el nuevo usuario
        usuario = Usuario.objects.create_user(nombre=nombre, email=email, password=password)
        usuario.save()

        # Iniciar sesión automáticamente después de registrarse
        login(request, usuario)

        return redirect('Libreria Aprendamos')  # Redirige a la página principal o al dashboard

    return render(request, 'login.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Autenticamos manualmente
        usuario = authenticate(request, username=email, password=password)
        print(email, password)
        print(usuario is not None)
        
        if usuario is not None:
            login(request, usuario)
            return redirect('Libreria Aprendamos')  # Redirigir a la página principal
        else:
            # Si la autenticación falla
            error = "Credenciales inválidas"
            return render(request, 'login.html', {'error': error})
    
    return render(request, 'login.html')

@login_required
def dashboard_view(request):
    usuario_actual = request.user  # Aquí puedes acceder a 'id', 'nombre', 'email', etc.
    return render(request, 'main.html', {'usuario': usuario_actual})



#Libros


@login_required
def agregar_documento(request):
     
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            archivo = form.cleaned_data['archivo']
            
            # Subir el archivo a S3
            nombre_archivo_s3 = f"documentos/{request.user.nombre}/{archivo.name}"
            url_archivo_s3 = subir_archivo_s3(archivo, nombre_archivo_s3)
            
            if url_archivo_s3:
                # Guardar en la base de datos
                Documento.objects.create(
                    usuario=request.user,
                    nombre=nombre,
                    archivo=nombre_archivo_s3  # Guardamos la URL en lugar del archivo
                )
                return redirect('Libreria Aprendamos')
            else:
                form.add_error(None, "Hubo un problema subiendo el archivo a S3.")
    else:
        form = DocumentoForm()

    return render(request, 'agregar.html', {'form': form})

def listar_documentos(request):
    usuario_actual = request.user
    
    documentos = Documento.objects.all()
    for documento in documentos:
        documento.enlace_prefirmado = obtener_enlace_prefirmado(documento.archivo)  # Generar el enlace
        print(documento.archivo)

    return render(request, 'main.html', {'documentos': documentos, 'usuario': usuario_actual})

def obtener_enlace_prefirmado(nombre_archivo):
    mm = 'documentos/leo/PRESENTACIÓN DE DISEÑO DE BASE DE DATOS A.pdf'
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    
    try:
        enlace_prefirmado = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': nombre_archivo,
            },
            ExpiresIn=3600  # El enlace será válido por 1 hora
        )
        return enlace_prefirmado
    except NoCredentialsError:
        print("Credenciales no encontradas")
        return None
 
