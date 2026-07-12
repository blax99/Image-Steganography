from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .forms import EncodeForm, DecodeForm
from .models import StegoOperation
from encryption import SteganographyService
import io
import os
import tempfile
import uuid

service = SteganographyService()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_temp_path(filename):
    """Get cross-platform temporary file path."""
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, filename)


def save_uploaded_image(uploaded_file):
    """Persist an uploaded image to disk and return its temporary path."""
    unique_filename = f"{uuid.uuid4()}_{uploaded_file.name}"
    image_path = get_temp_path(unique_filename)
    with open(image_path, 'wb') as handle:
        for chunk in uploaded_file.chunks():
            handle.write(chunk)
    return image_path


@login_required(login_url='login')
def home(request):
    user_stats = {
        'total_operations': StegoOperation.objects.filter(user=request.user).count(),
        'encode_count': StegoOperation.objects.filter(user=request.user, operation_type='encode').count(),
        'decode_count': StegoOperation.objects.filter(user=request.user, operation_type='decode').count(),
    }
    return render(request, 'stego/home.html', user_stats)

@login_required(login_url='login')
def encode_image(request):
    if request.method == 'POST':
        form = EncodeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                image = request.FILES['image']
                message = form.cleaned_data['message']
                secret_key = form.cleaned_data['secret_key']
                
                image_path = save_uploaded_image(image)
                output_path = get_temp_path(f"{uuid.uuid4().hex}.png")
                service.encode_message(message, secret_key, image_path, output_path)

                with open(output_path, 'rb') as handle:
                    payload = handle.read()

                StegoOperation.objects.create(
                    user=request.user,
                    operation_type='encode',
                    original_filename=image.name,
                    message_length=len(message),
                    status='success',
                    ip_address=get_client_ip(request)
                )

                try:
                    if os.path.exists(image_path):
                        os.remove(image_path)
                    if os.path.exists(output_path):
                        os.remove(output_path)
                except Exception as cleanup_error:
                    print(f"Cleanup warning: {cleanup_error}")

                response = HttpResponse(payload, content_type='image/png')
                response['Content-Disposition'] = 'attachment; filename="encoded_image.png"'
                messages.success(request, 'Image encoded successfully! Download started.')
                return response
            
            except Exception as e:
                error_msg = str(e)
                image_name = image.name if 'image' in locals() else 'unknown'
                
                # Log failed operation
                StegoOperation.objects.create(
                    user=request.user,
                    operation_type='encode',
                    original_filename=image_name,
                    status='error',
                    error_message=error_msg,
                    ip_address=get_client_ip(request)
                )
                
                # Clean up temp file if it exists
                try:
                    if 'image_path' in locals() and os.path.exists(image_path):
                        os.remove(image_path)
                except:
                    pass
                
                messages.error(request, f'Error encoding image: {error_msg}')
    else:
        form = EncodeForm()
    
    return render(request, 'encode.html', {'form': form})

@login_required(login_url='login')
def decode_image(request):
    if request.method == 'POST':
        form = DecodeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                image = request.FILES['image']
                secret_key = form.cleaned_data['secret_key']
                
                image_path = save_uploaded_image(image)
                try:
                    decoded_message = service.decode_message(image_path, secret_key)
                except Exception as decoding_error:
                    decoded_message = None
                    error_message = str(decoding_error)
                else:
                    error_message = None

                try:
                    if os.path.exists(image_path):
                        os.remove(image_path)
                except Exception as cleanup_error:
                    print(f"Cleanup warning: {cleanup_error}")

                if decoded_message is None:
                    StegoOperation.objects.create(
                        user=request.user,
                        operation_type='decode',
                        original_filename=image.name,
                        status='error',
                        error_message=error_message or 'Invalid secret key or corrupted image',
                        ip_address=get_client_ip(request)
                    )
                    messages.error(request, 'Invalid secret key or corrupted image.')
                else:
                    StegoOperation.objects.create(
                        user=request.user,
                        operation_type='decode',
                        original_filename=image.name,
                        message_length=len(decoded_message),
                        status='success',
                        ip_address=get_client_ip(request)
                    )
                    return render(request, 'decode.html', {
                        'form': form,
                        'decoded_message': decoded_message,
                        'success': True
                    })
            
            except Exception as e:
                error_msg = str(e)
                image_name = image.name if 'image' in locals() else 'unknown'
                
                # Log failed operation
                StegoOperation.objects.create(
                    user=request.user,
                    operation_type='decode',
                    original_filename=image_name,
                    status='error',
                    error_message=error_msg,
                    ip_address=get_client_ip(request)
                )
                
                # Clean up temp file if it exists
                try:
                    if 'image_path' in locals() and os.path.exists(image_path):
                        os.remove(image_path)
                except:
                    pass
                
                messages.error(request, f'Error decoding image: {error_msg}')
    else:
        form = DecodeForm()
    
    return render(request, 'decode.html', {'form': form})

@login_required(login_url='login')
def operation_history(request):
    if not request.user.is_authenticated:
        return redirect('login')

    operations = StegoOperation.objects.filter(
        user=request.user
    ).order_by('-created_at')[:20]

    return render(request, 'history.html', {
        'operations': operations
    })