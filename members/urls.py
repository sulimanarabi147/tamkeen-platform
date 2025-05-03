from django.urls import path
from .views import public_profile
from .views import contact_member
from django.urls import path
from .views import statistics_view
from django.urls import path
from . import views

urlpatterns = [
    path('member/<str:serial_number>/', public_profile, name='public_profile'),
    path('member/<str:serial_number>/contact/', contact_member, name='contact_member'),
    path('admin/member_statistics/', statistics_view, name='member_statistics'),
    path('statistics/', statistics_view, name='statistics_view'),  # تعديل المسار إذا كان ضروريًا
    path('member/<str:serial_number>/', views.member_detail, name='member_detail'),  # عرض تفاصيل العضو
]
