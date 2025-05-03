from django.db import models
from django.utils import timezone
from django.core.files import File
from io import BytesIO
import qrcode

# خيارات العضوية
class MemberRole(models.TextChoices):
    PRESIDENT = 'president', 'رئيس المجلس'
    VICE_PRESIDENT = 'vice_president', 'نائب الرئيس'
    ACADEMIC_AGENT = 'academic_agent', 'الوكيل الأكاديمي'
    ADMIN_AGENT = 'admin_agent', 'الوكيل الإداري'
    DEPT_HEAD = 'department_head', 'رئيس قسم'
    DEPT_MEMBER = 'department_member', 'عضو قسم'
    ACTIVE_MEMBER = 'active_member', 'عضو نشط'
    REGULAR_MEMBER = 'regular_member', 'عضو منتسب'

class Member(models.Model):
    ROLES = [
        ('president', 'رئيس المجلس'),
        ('vice_president', 'نائب الرئيس'),
        ('academic_dean', 'الوكيل الأكاديمي'),
        ('admin_dean', 'الوكيل الإداري'),
        ('department_head', 'رئيس قسم'),
        ('department_member', 'عضو قسم'),
        ('active_member', 'عضو نشط'),
        ('affiliate_member', 'عضو منتسب'),
    ]

    full_name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50, unique=True)
    role = models.CharField(choices=ROLES, max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    join_date = models.DateField(null=True, blank=True)  # تم تعديل الحقل ليكون قابلًا للتعديل
    department = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)  # حقل تفعيل العضوية
    profile_url = models.URLField(max_length=200, blank=True, null=True)  # حقل الرابط الخاص بالعضو
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)  # حقل qr code
    show_public_profile = models.BooleanField(default=True)  # أضفنا هذا الحقل

    def __str__(self):
        return self.full_name

    def get_role_display(self):
        return dict(self.ROLES).get(self.role, '')

    def generate_profile_url(self):
        # توليد رابط العضو بناءً على الرقم التسلسلي
        base_url = "http://127.0.0.1:8000/member/"
        return f"{base_url}{self.serial_number}/"

    def generate_qr_code(self):
        # توليد QR Code لعرض الرابط
        profile_url = self.generate_profile_url()
        qr = qrcode.make(profile_url)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        filename = f"{self.serial_number}_qr.png"
        filebuffer = File(buffer, name=filename)
        self.qr_code_image.save(filename, filebuffer, save=False)

    def save(self, *args, **kwargs):
        if not self.profile_url:
            self.profile_url = self.generate_profile_url()
        if not self.qr_code_image:
            self.generate_qr_code()
        super().save(*args, **kwargs)
