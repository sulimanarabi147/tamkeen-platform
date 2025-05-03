from django.contrib import admin
from django.db.models import Count
from .models import Member
from import_export import resources
from import_export.admin import ExportMixin

class MemberResource(resources.ModelResource):
    class Meta:
        model = Member
        fields = ('id', 'full_name', 'serial_number', 'role', 'department', 'is_active', 'join_date', 'profile_url')  # إضافة الرابط المخصص
        export_order = ('full_name', 'serial_number', 'role', 'department', 'is_active', 'join_date', 'profile_url')  # ترتيب الحقول في التصدير

class MemberAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('full_name', 'serial_number', 'role', 'is_active', 'join_date', 'profile_url')  # إضافة profile_url لعرضه في القائمة
    list_filter = ('role', 'is_active')
    search_fields = ('full_name', 'serial_number')
    actions = ['activate_members', 'deactivate_members']
    resource_class = MemberResource

    # إضافة join_date للحقل القابل للتعديل
    list_editable = ('join_date',)

    def activate_members(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "تم تفعيل الأعضاء المختارين.")

    def deactivate_members(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "تم تعطيل الأعضاء المختارين.")

    activate_members.short_description = "تفعيل الأعضاء"
    deactivate_members.short_description = "تعطيل الأعضاء"

    def changelist_view(self, request, extra_context=None):
        stats = self.get_stats()
        extra_context = extra_context or {}
        extra_context['stats'] = stats
        return super().changelist_view(request, extra_context=extra_context)

    def get_stats(self):
        total_members = Member.objects.count()
        active_members = Member.objects.filter(is_active=True).count()
        inactive_members = total_members - active_members
        role_counts = Member.objects.values('role').annotate(count=Count('role'))
        department_counts = Member.objects.values('department').annotate(count=Count('department'))

        stats = {
            'total_members': total_members,
            'active_members': active_members,
            'inactive_members': inactive_members,
            'role_counts': role_counts,
            'department_counts': department_counts,
        }

        return stats

admin.site.register(Member, MemberAdmin)
