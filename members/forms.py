from django import forms

class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=100, label="اسم المرسل")
    email = forms.EmailField(label="البريد الإلكتروني")
    message = forms.CharField(widget=forms.Textarea, label="الرسالة")
