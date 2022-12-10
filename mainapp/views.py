from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DetailView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, FileResponse, HttpResponseRedirect
from django.template.loader import render_to_string

from mainapp import tasks
from mainapp.models import News, Courses, CourseFeedback
from mainapp import models as mainapp_models
from mainapp.forms import CourseFeedBackForm


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageView(ListView):
    model = News
    template_name = "mainapp/news_list.html"
    paginate_by = 5
    ordering = '-id'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(deleted=False)


class NewsDetailView(DetailView):
    model = News


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.add_news',)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.change_news',)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.delete_news',)


class LoginPageView(TemplateView):
    template_name = "authapp/login.html"


class CoursesListView(ListView):
    model = Courses
    paginate_by = 5
    ordering = ['-pk']


class CoursesDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super(CoursesDetailView, self).get_context_data(**kwargs)
        context["course_object"] = get_object_or_404(mainapp_models.Courses, pk=pk)
        context["lessons"] = mainapp_models.Lesson.objects.filter(course=context["course_object"])
        context["teachers"] = mainapp_models.CourseTeachers.objects.filter(course=context["course_object"])

        feedback_list_key = f'course_feedback_{context["course_object"].pk}'
        cached_feedback_list = cache.get(feedback_list_key)

        if cached_feedback_list is None:
            context["feedback_list"] = mainapp_models.CourseFeedback.objects.filter(course=context["course_object"],
                                                                                    deleted=False)
            cache.set(feedback_list_key, context["feedback_list"], timeout=300)
        else:
            context["feedback_list"] = cached_feedback_list

        if self.request.user.is_authenticated:
            is_commented = mainapp_models.CourseFeedback.objects.filter(course=context["course_object"],
                                                                        user=self.request.user,
                                                                        deleted=False).first()
            if not is_commented:
                context['feedback_form'] = CourseFeedBackForm(
                    course=context["course_object"],
                    user=self.request.user,
                )

        return context


class CourseFeedbackCreateView(CreateView):
    model = CourseFeedback
    form_class = CourseFeedBackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_template = render_to_string('mainapp/includes/feedback_card.html', context={'item': self.object})
        return JsonResponse({'card': rendered_template})


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"

    def post(self, *args, **kwargs):
        # delay делает задачу отложенной (чтобы она попадала в общую очередь задач)
        message_from = self.request.POST.get('message_from')
        message_body = self.request.POST.get('message_body')
        tasks.send_feedback_to_email.delay(message_from, message_body)

        return HttpResponseRedirect(reverse_lazy('mainapp:contacts'))


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class LogView(UserPassesTestMixin, TemplateView):
    template_name = 'mainapp/logs.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        log_lines = []
        with open(settings.BASE_DIR / 'log/main_log.log') as log_file:
            for i, line in enumerate(log_file):
                if i == 1000:
                    break
                log_lines.insert(0, line)

            context_data['logs'] = log_lines
        return context_data


class LogDownloadView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, 'rb'))
