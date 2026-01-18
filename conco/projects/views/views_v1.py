from django.views import View
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.http import Http404
from django.utils.translation import gettext as _, activate

from projects.models import Appeal
from projects.forms.forms_v1 import AppealForm
from projects.utils.queries import *


class HomePageView(View):
    template_name = 'index.html'
    
    def get(self, request):
        lang = get_language_from_request(request)
        activate(lang)
        context = get_home_page_data(request, lang)
        context['language'] = lang
        return render(request, self.template_name, context)


class ProjectPageView(View):
    template_name = 'projects.html'
    
    def get(self, request):
        lang = get_language_from_request(request)
        activate(lang)
        context = get_project_list_data(request, lang)
        context['language'] = lang
        return render(request, self.template_name, context)


class ProjectDetailPageView(View):
    template_name = 'project-details.html'
    
    def get(self, request, slug):
        lang = get_language_from_request(request)
        activate(lang)
        project = get_project_by_slug(slug, lang)
        if not project:
            raise Http404(_("Project not found"))
        
        context = {
            'project': serialize_project(project, lang),
            'language': lang,
            'background_image': get_background_image('project'),
        }

        return render(request, self.template_name, context)


class AboutPageView(View):
    template_name = 'about.html'
    
    def get(self, request):
        lang = get_language_from_request(request)
        is_active = request.GET.get('is_active', 'true').lower() == 'true'
        activate(lang)
        about = get_about(lang)
        partners = get_partners(lang=lang, is_active=is_active)
        context = {
            'about': serialize_about(about, lang) if about else None,
            'partners': [serialize_partner(p, lang) for p in partners],
            'language': lang,
            'background_image': get_background_image('about'),
        }

        return render(request, self.template_name, context)


class ContactPageView(View):
    template_name = 'contact.html'
    
    def get(self, request):
        lang = get_language_from_request(request)
        activate(lang)
        contact = get_contact(lang)
        context = {
            'contact': serialize_contact(contact, lang) if contact else None,
            'language': lang,
        }

        return render(request, self.template_name, context)


class VacancyPageView(View):
    template_name = 'vacancy.html'
    
    def get(self, request):
        lang = get_language_from_request(request)
        activate(lang)
        context = get_vacancy_list_data(request, lang)
        context['language'] = lang
        return render(request, self.template_name, context)


class VacancyDetailPageView(View):
    template_name = 'vacancy-details.html'
    
    def get(self, request, slug):
        lang = get_language_from_request(request)
        activate(lang)
        vacancy = get_vacancy_by_slug(slug, lang)
        if not vacancy:
            from django.http import Http404
            raise Http404(_("Vacancy not found"))
        
        form = AppealForm()
        context = {
            'vacancy': serialize_vacancy(vacancy, lang),
            'language': lang,
            'background_image': get_background_image('vacancy'),
            'form': form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, slug):
        lang = get_language_from_request(request)
        activate(lang)
        vacancy = get_vacancy_by_slug(slug, lang)
        if not vacancy:
            raise Http404(_("Vacancy not found"))
        
        form = AppealForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            situation_one = Appeal.objects.filter(vacancy=vacancy, email=email).exists()
            situation_two = Appeal.objects.filter(vacancy=vacancy, phone_number=phone_number).exists()
            
            if situation_one or situation_two :
                messages.error(request, _('Bu vakansiyaya müraciət artıq göndərilmişdir.'))
            else:
                try:
                    appeal = form.save(commit=False)
                    appeal.vacancy = vacancy
                    appeal.save()
                    messages.success(request, _('Müraciətiniz uğurla göndərildi.'))
                    return redirect('projects:vacancy-detail', slug=slug)
                except IntegrityError:
                    messages.error(request, _('Bu e-poçt ünvanı ilə bu vakansiyaya müraciət artıq göndərilmişdir.'))
        else:
            messages.error(request, _('Xəta baş verdi. Zəhmət olmasa yenidən cəhd edin.'))
        
        context = {
            'vacancy': serialize_vacancy(vacancy, lang),
            'language': lang,
            'background_image': get_background_image('vacancy'),
            'form': form,
        }
        return render(request, self.template_name, context)


