from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
from .forms import EncodeForm, DecodeForm
from .models import StegoOperation
from . import utils
import io
import os
import tempfile
from pathlib import Path

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_temp_path(filename):
    """Get cross-platform temporary file path"""
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, filename)

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
                
                # Create unique filename to avoid conflicts
                import uuid
                unique_filename = f"{uuid.uuid4()}_{image.name}"
                image_path = get_temp_path(unique_filename)
                
                # Save uploaded image to temp directory
                with open(image_path, 'wb') as f:
                    for chunk in image.chunks():
                        f.write(chunk)
                
                # Encrypt and hide message in image
                encrypted_message = utils.encrypt_message(message, secret_key)
                stego_image = utils.hide_message_in_image(image_path, encrypted_message)
                
                # Save encoded image to bytes
                output = io.BytesIO()
                stego_image.save(output, format='PNG')
                output.seek(0)
                
                # Log operation to database
                StegoOperation.objects.create(
                    user=request.user,
                    operation_type='encode',
                    original_filename=image.name,
                    message_length=len(message),
                    status='success',
                    ip_address=get_client_ip(request)
                )
                
                # Clean up temp file
                try:
                    if os.path.exists(image_path):
                        os.remove(image_path)
                except Exception as cleanup_error:
                    print(f"Cleanup warning: {cleanup_error}")
                
                # Return encoded image as download
                response = HttpResponse(output.getvalue(), content_type='image/png')
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
                
                # Create unique filename to avoid conflicts
                import uuid
                unique_filename = f"{uuid.uuid4()}_{image.name}"
                image_path = get_temp_path(unique_filename)
                
                # Save uploaded image to temp directory
                with open(image_path, 'wb') as f:
                    for chunk in image.chunks():
                        f.write(chunk)
                
                # Extract and decrypt message from image
                encrypted_message = utils.extract_message_from_image(image_path)
                decrypted_message = utils.decrypt_message(encrypted_message, secret_key)
                
                # Clean up temp file
                try:
                    if os.path.exists(image_path):
                        os.remove(image_path)
                except Exception as cleanup_error:
                    print(f"Cleanup warning: {cleanup_error}")
                
                if decrypted_message is None:
                    # Log failed decode operation
                    StegoOperation.objects.create(
                        user=request.user,
                        operation_type='decode',
                        original_filename=image.name,
                        status='error',
                        error_message='Invalid secret key or corrupted image',
                        ip_address=get_client_ip(request)
                    )
                    messages.error(request, 'Invalid secret key or corrupted image.')
                else:
                    # Log successful decode operation
                    StegoOperation.objects.create(
                        user=request.user,
                        operation_type='decode',
                        original_filename=image.name,
                        message_length=len(decrypted_message),
                        status='success',
                        ip_address=get_client_ip(request)
                    )
                    
                    return render(request, 'decode.html', {
                        'form': form,
                        'decoded_message': decrypted_message,
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