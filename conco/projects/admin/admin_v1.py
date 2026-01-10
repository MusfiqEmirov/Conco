from django.contrib import admin
from projects.models import *

# Media 
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'about',
        'project',
        'partner',
        'vacancy',
        'is_home_page_background_image',
        'is_about_page_background_image',
        'is_partner_background_image',
        'is_project_page_background_image',
        'created_at',
    )
    list_filter = (
        'is_home_page_background_image',
        'is_about_page_background_image',
        'is_partner_background_image',
        'is_project_page_background_image',
        'created_at',
    )
    readonly_fields = ('created_at',)


class MediaInlineBase(admin.TabularInline):
    model = Media
    extra = 1
    readonly_fields = ('created_at',)
    fields = (
        'image',
    )


class MediaInlineProject(MediaInlineBase):
    fields = MediaInlineBase.fields + ('video',)


class MediaInlinePartner(MediaInlineBase):
    pass


class MediaInlineAbout(MediaInlineBase):
    pass


class MediaInlineVacancy(MediaInlineBase):
    max_num = 1  

# Project Category 
@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_az',)
    search_fields = ('name_az', 'name_en', 'name_ru')

# Project 
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name_az',
        'category',
        'is_completed',
        'is_active',
        'created_at',
    )
    list_filter = (
        'category',
        'is_completed',
        'is_active',
        'created_at',
    )
    search_fields = ('name_az', 'name_en', 'name_ru', 'description_az', 'description_en', 'description_ru')
    exclude = ('slug',)
    inlines = [MediaInlineProject]

# Partner 
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = (
        'name_az',
        'url',
        'is_active',
        'created_at',
    )
    list_filter = ('is_active', 'created_at')
    search_fields = ('name_az', 'name_en', 'name_ru')
    ordering = ('-created_at',)
    inlines = [MediaInlinePartner]

# About 
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('main_title_az', 'second_title_az')
    search_fields = ('main_title_az', 'second_title_az', 'description_az')
    inlines = [MediaInlineAbout]

# Contact 
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'address_az',
        'phone',
        'email',
    )
    search_fields = (
        'address_az',
        'phone',
        'email',
    )

# Vacancy 
@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    inlines = [MediaInlineVacancy]
    list_display = (
        'title_az',
        'is_active',
        'created_at',
    )
    list_filter = ('is_active', 'created_at')
    search_fields = ('title_az', 'title_en', 'title_ru', 'description_az', 'description_en', 'description_ru')
    exclude = ('slug',)

# Appeal (CV) 
@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = (
        'vacancy',
        'cv',
        'is_read',
        'created_at',
    )
    list_filter = ('is_read', 'created_at')
    readonly_fields = ('created_at',)
