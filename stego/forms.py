from django import forms

class EncodeForm(forms.Form):
    image = forms.ImageField(
        label='Select Image (PNG/JPG)',
        widget=forms.FileInput(attrs={'accept': 'image/png, image/jpeg'})
    )
    message = forms.CharField(
        label='Secret Message',
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter your secret message here'}),
        max_length=5000
    )
    secret_key = forms.CharField(
        label='Secret Key',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter a strong secret key'}),
        min_length=8
    )

class DecodeForm(forms.Form):
    image = forms.ImageField(
        label='Select Encoded Image',
        widget=forms.FileInput(attrs={'accept': 'image/png, image/jpeg'})
    )
    secret_key = forms.CharField(
        label='Secret Key',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter the secret key used for encoding'}),
        min_length=8
    )