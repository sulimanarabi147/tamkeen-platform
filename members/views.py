from django.shortcuts import render, get_object_or_404
from django.db import models
from django.core.mail import send_mail
from django.conf import settings

from .models import Member
from .forms import ContactForm

# الصفحة الرئيسية - البحث عن عضو من خلال الرقم التسلسلي
def home(request):
    member = None
    serial = ''

    if request.method == 'POST':
        serial = request.POST.get('serial_number')
        try:
            member = Member.objects.get(serial_number=serial)
        except Member.DoesNotExist:
            member = None

    return render(request, 'home.html', {'member': member, 'serial': serial})

# عرض تفاصيل العضو بناءً على الرقم التسلسلي
def member_detail(request, serial_number):
    # الحصول على عضو بناءً على الرقم التسلسلي
    member = get_object_or_404(Member, serial_number=serial_number)
    
    # تمرير البيانات إلى الـ template
    return render(request, 'member_detail.html', {'member': member})

# عرض الملف الشخصي العام للعضو (في حال تم تفعيل إظهاره للناس)
def public_profile(request, serial_number):
    member = get_object_or_404(Member, serial_number=serial_number, is_active=True, show_public_profile=True)
    return render(request, 'members/public_profile.html', {'member': member})

# تواصل مع عضو معين
def contact_member(request, serial_number):
    member = get_object_or_404(Member, serial_number=serial_number)
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            subject = f"طلب تواصل مع {member.full_name}"
            body = f"المرسل: {full_name}\nالبريد: {email}\nالرسالة:\n{message}"
            
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])
            
            return render(request, 'members/contact_success.html', {'member': member})
    else:
        form = ContactForm()

    return render(request, 'members/contact_form.html', {'form': form, 'member': member})

# إحصائيات الأعضاء (نسخة مخصصة للإدارة)
def admin_member_statistics(request):
    total_members = Member.objects.count()
    active_members = Member.objects.filter(is_active=True).count()
    inactive_members = total_members - active_members

    role_counts = Member.objects.values('role').annotate(count=models.Count('role'))
    department_counts = Member.objects.values('department').annotate(count=models.Count('department'))

    stats = {
        'total_members': total_members,
        'active_members': active_members,
        'inactive_members': inactive_members,
        'role_counts': role_counts,
        'department_counts': department_counts
    }

    return render(request, 'admin/member_statistics.html', {'stats': stats})

# نسخة أخرى لعرض الإحصائيات في صفحة مختلفة إن لزم الأمر
def statistics_view(request):
    total_members = Member.objects.count()
    active_members = Member.objects.filter(is_active=True).count()
    inactive_members = total_members - active_members

    role_counts = Member.objects.values('role').annotate(count=models.Count('role'))
    department_counts = Member.objects.values('department').annotate(count=models.Count('department'))

    stats = {
        'total_members': total_members,
        'active_members': active_members,
        'inactive_members': inactive_members,
        'role_counts': role_counts,
        'department_counts': department_counts
    }

    return render(request, 'admin/statistics_view.html', {'stats': stats})
