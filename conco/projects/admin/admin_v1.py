from django.contrib import admin
from django.db.models import Q
from django.db import models
from django.utils.html import format_html
from django.urls import reverse

from projects.models import *


# Media
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'media_preview',
        'background_flags',
        'created_at',
    )
    list_display_links = ('media_preview',)
    list_filter = (
        'is_home_page_background_image',
        'is_about_page_background_image',
        'is_partner_background_image',
        'is_project_page_background_image',
        'is_vacany_page_background_image',
        'created_at',
    )
    readonly_fields = ('created_at', 'media_preview_detailed')

    fieldsets = (
        ('Media Faylı', {
            'fields': ('image', 'media_preview_detailed')
        }),
        ('Arxa Plan Təyinatları', {
            'fields': (
                'is_home_page_background_image',
                'is_about_page_background_image',
                'is_partner_background_image',
                'is_project_page_background_image',
                'is_vacany_page_background_image',
            ),
        }),
    )

    ordering = ('-created_at',)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(
            models.Q(is_home_page_background_image=True) |
            models.Q(is_about_page_background_image=True) |
            models.Q(is_partner_background_image=True) |
            models.Q(is_project_page_background_image=True) |
            models.Q(is_vacany_page_background_image=True)
        )

    def media_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 80px; max-height: 80px; border-radius: 4px;" />',
                obj.image.url
            )
        return "-"
    media_preview.short_description = "Şəkil"

    def media_preview_detailed(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 8px;" />',
                obj.image.url
            )
        return "-"
    media_preview_detailed.short_description = "Şəkil Önizləmə"

    def background_flags(self, obj):
        flags = []
        if obj.is_home_page_background_image:
            flags.append("🏠 Ana səhifə")
        if obj.is_about_page_background_image:
            flags.append("ℹ️ Haqqımızda səhifəsi")
        if obj.is_partner_background_image:
            flags.append("🤝 Əməkdaşlar səhifəi")
        if obj.is_project_page_background_image:
            flags.append("📁 Layihələr səhifəsi")
        if obj.is_vacany_page_background_image:
            flags.append("💼 Vakansiyalar səhifəsi")
        return " | ".join(flags) if flags else "-"
    background_flags.short_description = "Arxa Plan"



class MediaInlineBase(admin.TabularInline):
    model = Media
    extra = 1
    readonly_fields = ('created_at', 'thumbnail_preview')
    fields = ('image', 'video', 'thumbnail_preview', 'created_at')
    verbose_name = "Media"
    verbose_name_plural = "Medialar"
    
    def thumbnail_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-width: 60px; max-height: 60px; border-radius: 4px;" />',
                obj.image.url
            )
        return "-"
    thumbnail_preview.short_description = "Önizləmə"


class MediaInlineProject(MediaInlineBase):
    fields = ('image', 'video', 'thumbnail_preview', 'created_at')


class MediaInlinePartner(MediaInlineBase):
    fields = ('image', 'thumbnail_preview', 'created_at')


class MediaInlineAbout(MediaInlineBase):
    fields = ('image', 'thumbnail_preview', 'created_at')


class MediaInlineVacancy(MediaInlineBase):
    max_num = 1
    fields = ('image', 'thumbnail_preview', 'created_at')  

# Project Category 
@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_link', 'name_en', 'name_ru', 'projects_count')
    list_display_links = None
    search_fields = ('name_az', 'name_en', 'name_ru')
    list_per_page = 25
    
    fieldsets = (
        ('Azərbaycan', {
            'fields': ('name_az',)
        }),
        ('English', {
            'fields': ('name_en',)
        }),
        ('Русский', {
            'fields': ('name_ru',)
        }),
    )
    
    def name_link(self, obj):
        url = reverse('admin:projects_projectcategory_change', args=[obj.pk])
        name = obj.name_az or 'Kateqoriya'
        return format_html('<a href="{}" style="color: #417690; text-decoration: none; font-weight: 600; font-size: 14px;">🔗 {}</a>', url, name)
    name_link.short_description = "Ad (AZ)"
    name_link.admin_order_field = 'name_az'
    
    def projects_count(self, obj):
        count = obj.projects.count()
        if count > 0:
            url = reverse('admin:projects_project_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}" style="color: #28a745; text-decoration: none;">📁 {} layihə</a>', url, count)
        return "0 layihə"
    projects_count.short_description = "Layihələr"

# Project 
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name_link',
        'category',
        'status_badges',
        'created_at',
    )
    list_display_links = None
    list_filter = (
        'category',
        'is_completed',
        'is_active',
        'created_at',
    )
    search_fields = ('name_az', 'name_en', 'name_ru', 'description_az', 'description_en', 'description_ru')
    exclude = ('slug',)
    inlines = [MediaInlineProject]
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('category', 'url')
        }),
        ('Azərbaycan', {
            'fields': ('name_az', 'description_az')
        }),
        ('English', {
            'fields': ('name_en', 'description_en')
        }),
        ('Русский', {
            'fields': ('name_ru', 'description_ru')
        }),
        ('Status', {
            'fields': ('is_completed', 'is_active')
        }),
        ('Tarix', {
            'fields': ('created_at',)
        }),
    )
    
    def name_link(self, obj):
        url = reverse('admin:projects_project_change', args=[obj.pk])
        return format_html('<a href="{}" style="color: #417690; text-decoration: none; font-weight: 600; font-size: 14px;">🔗 {}</a>', url, obj.name_az)
    name_link.short_description = "Layihə Adı"
    name_link.admin_order_field = 'name_az'
    
    def status_badges(self, obj):
        badges = []
        if obj.is_active:
            badges.append('<span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">✓ Aktiv</span>')
        else:
            badges.append('<span style="background: #dc3545; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">✗ Deaktiv</span>')
        
        if obj.is_completed:
            badges.append('<span style="background: #17a2b8; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">✓ Tamamlanıb</span>')
        else:
            badges.append('<span style="background: #ffc107; color: #333; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">🔄 Davam edir</span>')
        
        return format_html(' '.join(badges))
    status_badges.short_description = "Status"

# Partner 
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'partner_logo',
        'name_link',
        'url_link',
        'active_status',
        'created_at',
    )
    list_display_links = None
    list_filter = ('is_active', 'created_at')
    search_fields = ('name_az', 'name_en', 'name_ru')
    ordering = ('-created_at',)
    inlines = [MediaInlinePartner]
    readonly_fields = ('created_at', 'logo_preview')
    list_per_page = 25
    
    fieldsets = (
        ('Azərbaycan', {
            'fields': ('name_az',)
        }),
        ('English', {
            'fields': ('name_en',)
        }),
        ('Русский', {
            'fields': ('name_ru',)
        }),
        ('Əlaqə', {
            'fields': ('url',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Media', {
            'fields': ('logo_preview',)
        }),
        ('Tarix', {
            'fields': ('created_at',)
        }),
    )
    
    def partner_logo(self, obj):
        media = obj.medias.first()
        if media and media.image:
            return format_html(
                '<img src="{}" style="max-width: 60px; max-height: 60px; border-radius: 4px; object-fit: contain;" />',
                media.image.url
            )
        return "❌"
    partner_logo.short_description = "Logo"
    
    def name_link(self, obj):
        url = reverse('admin:projects_partner_change', args=[obj.pk])
        name = obj.name_az or 'Əməkdaş'
        return format_html('<a href="{}" style="color: #417690; text-decoration: none; font-weight: 600; font-size: 14px;">🔗 {}</a>', url, name)
    name_link.short_description = "Ad"
    name_link.admin_order_field = 'name_az'
    
    def logo_preview(self, obj):
        media = obj.medias.first()
        if media and media.image:
            return format_html(
                '<img src="{}" style="max-width: 250px; max-height: 250px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                media.image.url
            )
        return "Logo yoxdur"
    logo_preview.short_description = "Logo Önizləmə"
    
    def url_link(self, obj):
        if obj.url:
            return format_html('<a href="{}" target="_blank" style="color: #417690; text-decoration: none;">🔗 Link</a>', obj.url)
        return "-"
    url_link.short_description = "URL"
    
    def active_status(self, obj):
        if obj.is_active:
            return format_html('<span style="background: #28a745; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">✓ Aktiv</span>')
        return format_html('<span style="background: #dc3545; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">✗ Deaktiv</span>')
    active_status.short_description = "Status"

# About 
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_link', 'second_title_az', 'media_count', 'updated_info')
    list_display_links = None
    search_fields = ('main_title_az', 'main_title_en', 'main_title_ru', 'second_title_az', 'second_title_en', 'second_title_ru', 'description_az', 'description_en', 'description_ru')
    inlines = [MediaInlineAbout]
    list_per_page = 25
    
    fieldsets = (
        ('Əsas Başlıq', {
            'fields': ('main_title_az', 'main_title_en', 'main_title_ru')
        }),
        ('Alt Başlıq', {
            'fields': ('second_title_az', 'second_title_en', 'second_title_ru')
        }),
        ('Təsvir - Azərbaycan', {
            'fields': ('description_az',)
        }),
        ('Təsvir - English', {
            'fields': ('description_en',)
        }),
        ('Təsvir - Русский', {
            'fields': ('description_ru',)
        }),
    )
    
    def title_link(self, obj):
        url = reverse('admin:projects_about_change', args=[obj.pk])
        title = obj.main_title_az or 'Haqqımızda'
        return format_html('<a href="{}" style="color: #417690; text-decoration: none; font-weight: 600; font-size: 14px;">🔗 {}</a>', url, title)
    title_link.short_description = "Əsas Başlıq"
    title_link.admin_order_field = 'main_title_az'
    
    def media_count(self, obj):
        count = obj.medias.count()
        if count > 0:
            return format_html('<span style="background: #007bff; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px;">📷 {} şəkil</span>', count)
        return "📷 0 şəkil"
    media_count.short_description = "Medialar"
    
    def updated_info(self, obj):
        if hasattr(obj, 'updated_at'):
            return obj.updated_at.strftime('%d.%m.%Y %H:%M') if obj.updated_at else "-"
        return "-"
    updated_info.short_description = "Son Yenilənmə"

# Contact 
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'address_link',
        'contact_phone',
        'contact_email',
        'social_links',
    )
    list_display_links = None
    search_fields = (
        'address_az', 'address_en', 'address_ru',
        'phone', 'whatsapp_number', 'whatsapp_number_2', 'phone_three',
        'email',
    )
    list_per_page = 25
    
    fieldsets = (
        ('Ünvan', {
            'fields': ('address_az', 'address_en', 'address_ru')
        }),
        ('Əlaqə Nömrələri', {
            'fields': ('phone', 'whatsapp_number', 'whatsapp_number_2', 'phone_three')
        }),
        ('Email', {
            'fields': ('email',)
        }),
        ('Sosial Şəbəkələr', {
            'fields': ('instagram', 'facebook', 'youtube', 'linkedn', 'tiktok')
        }),
    )
    
    def address_link(self, obj):
        url = reverse('admin:projects_contact_change', args=[obj.pk])
        address = obj.address_az or 'Əlaqə'
        return format_html('<a href="{}" style="color: #417690; text-decoration: none; font-weight: 600; font-size: 14px;">🔗 {}</a>', url, address[:50] + '...' if len(address) > 50 else address)
    address_link.short_description = "Ünvan"
    address_link.admin_order_field = 'address_az'
    
    def contact_phone(self, obj):
        phones = []
        if obj.phone:
            phones.append(format_html('<span style="color: #417690;">📞 {}</span>', obj.phone))
        if obj.whatsapp_number:
            phones.append(format_html('<span style="color: #25D366;">💬 {}</span>', obj.whatsapp_number))
        return format_html('<br>'.join(phones)) if phones else "-"
    contact_phone.short_description = "Telefonlar"
    
    def contact_email(self, obj):
        if obj.email:
            return format_html('<a href="mailto:{}" style="color: #417690; text-decoration: none;">✉️ {}</a>', obj.email, obj.email)
        return "-"
    contact_email.short_description = "Email"
    
    def social_links(self, obj):
        links = []
        if obj.instagram:
            links.append(format_html('<a href="{}" target="_blank" style="color: #E4405F; margin-right: 8px;">📷 Instagram</a>', obj.instagram))
        if obj.facebook:
            links.append(format_html('<a href="{}" target="_blank" style="color: #1877F2; margin-right: 8px;">👥 Facebook</a>', obj.facebook))
        if obj.youtube:
            links.append(format_html('<a href="{}" target="_blank" style="color: #FF0000; margin-right: 8px;">▶️ YouTube</a>', obj.youtube))
        if obj.linkedn:
            links.append(format_html('<a href="{}" target="_blank" style="color: #0A66C2; margin-right: 8px;">💼 LinkedIn</a>', obj.linkedn))
        if obj.tiktok:
            links.append(format_html('<a href="{}" target="_blank" style="color: #000000; margin-right: 8px;">🎵 TikTok</a>', obj.tiktok))
        return format_html(' '.join(links)) if links else "-"
    social_links.short_description = "Sosial Şəbəkələr"

# Vacancy 
@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    inlines = [MediaInlineVacancy]
    list_display = (
        'id',
        'title_link',
        'vacancy_status',
        'appeals_count',
        'created_at',
    )
    list_display_links = None
    list_filter = ('is_active', 'created_at')
    search_fields = ('title_az', 'title_en', 'title_ru', 'description_az', 'description_en', 'description_ru')
    exclude = ('slug',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Azərbaycan', {
            'fields': ('title_az', 'description_az')
        }),
        ('English', {
            'fields': ('title_en', 'description_en')
        }),
        ('Русский', {
            'fields': ('title_ru', 'description_ru')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Tarix', {
            'fields': ('created_at',)
        }),
    )
    
    def title_link(self, obj):
        url = reverse('admin:projects_vacancy_change', args=[obj.pk])
        return format_html('<a href="{}" style="color: #417690; text-decoration: none; font-weight: 600; font-size: 14px;">🔗 {}</a>', url, obj.title_az)
    title_link.short_description = "Vakansiya Adı"
    title_link.admin_order_field = 'title_az'
    
    def vacancy_status(self, obj):
        if obj.is_active:
            return format_html('<span style="background: #28a745; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">✓ Aktiv</span>')
        return format_html('<span style="background: #dc3545; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">✗ Deaktiv</span>')
    vacancy_status.short_description = "Status"
    
    def appeals_count(self, obj):
        count = obj.appeal_set.count()
        read_count = obj.appeal_set.filter(is_read=True).count()
        unread_count = count - read_count
        
        if count > 0:
            url = reverse('admin:projects_appeal_changelist') + f'?vacancy__id__exact={obj.id}'
            badge_html = f'<a href="{url}" style="text-decoration: none;">'
            if unread_count > 0:
                badge_html += f'<span style="background: #dc3545; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">📄 {count} CV ({unread_count} oxunmayıb)</span>'
            else:
                badge_html += f'<span style="background: #28a745; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">📄 {count} CV (hamısı oxunub)</span>'
            badge_html += '</a>'
            return format_html(badge_html)
        return format_html('<span style="color: #6c757d;">📄 0 CV</span>')
    appeals_count.short_description = "CV-lər"

# Appeal (CV) 
@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'is_read',
        'vacancy_title',
        'cv_file_link',
        'read_status',
        'created_at_formatted',
    )
    list_display_links = None
    list_editable = ('is_read',)
    list_filter = ('is_read', 'created_at', 'vacancy')
    readonly_fields = ('created_at', 'cv_preview')
    search_fields = ('vacancy__title_az', 'vacancy__title_en', 'vacancy__title_ru')
    ordering = ('-created_at',)
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Vakansiya', {
            'fields': ('vacancy',)
        }),
        ('CV Faylı', {
            'fields': ('cv', 'cv_preview')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
        ('Tarix', {
            'fields': ('created_at',)
        }),
    )
    
    def vacancy_title(self, obj):
        detail_url = reverse('admin:projects_appeal_change', args=[obj.pk])
        if obj.vacancy:
            vacancy_url = reverse('admin:projects_vacancy_change', args=[obj.vacancy.pk])
            return format_html(
                '<a href="{}" style="color: #417690; text-decoration: none; font-weight: 600; font-size: 14px; margin-right: 10px;">🔗 {}</a> '
                '<a href="{}" style="color: #6c757d; text-decoration: none; font-size: 11px;">💼 → Vakansiya</a>',
                detail_url, obj.vacancy.title_az, vacancy_url
            )
        return format_html('<a href="{}" style="color: #417690; text-decoration: none; font-weight: 600; font-size: 14px;">🔗 CV</a>', detail_url)
    vacancy_title.short_description = "Vakansiya"
    
    def cv_file_link(self, obj):
        detail_url = reverse('admin:projects_appeal_change', args=[obj.pk])
        file_name = obj.cv.name.split('/')[-1] if obj.cv else "CV"
        if obj.cv:
            return format_html(
                '<a href="{}" style="color: #417690; text-decoration: none; font-weight: 600; font-size: 14px; margin-right: 10px;">🔗 {}</a> '
                '<a href="{}" target="_blank" style="background: #007bff; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px; font-weight: bold;">📎 Aç</a>',
                detail_url, file_name, obj.cv.url
            )
        return format_html('<a href="{}" style="color: #417690; text-decoration: none; font-weight: 600; font-size: 14px;">🔗 CV</a>', detail_url)
    cv_file_link.short_description = "CV Faylı"
    
    def cv_preview(self, obj):
        if obj.cv:
            file_name = obj.cv.name.split('/')[-1]
            file_size = obj.cv.size if hasattr(obj.cv, 'size') else 'N/A'
            return format_html(
                '<div style="padding: 12px; background: #e3f2fd; border-radius: 4px; border-left: 3px solid #2196f3;">'
                '<span style="color: #1976d2; font-weight: 500;">📄 {}</span> '
                '<span style="color: #666; font-size: 12px;">({} KB)</span> '
                '<a href="{}" target="_blank" style="color: #2196f3; text-decoration: none; margin-left: 8px; font-weight: 500;">📥 Endir</a>'
                '</div>',
                file_name,
                round(file_size / 1024, 2) if isinstance(file_size, (int, float)) else file_size,
                obj.cv.url
            )
        return "-"
    cv_preview.short_description = "CV Önizləmə"
    
    def read_status(self, obj):
        if obj.is_read:
            return format_html('<span style="background: #28a745; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">✓ Oxunub</span>')
        return format_html('<span style="background: #dc3545; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">🔴 Oxunmayıb</span>')
    read_status.short_description = "Status"
    
    def created_at_formatted(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M') if obj.created_at else "-"
    created_at_formatted.short_description = "Tarix"


# Admin Site Customization
admin.site.site_header = "Conco Admin Panel"
admin.site.site_title = "Conco Admin"
admin.site.index_title = "Admin Paneli idarəetmə sistemi"
