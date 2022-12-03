from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DetailView, DeleteView
from mainapp.models import News, Courses, CourseFeedback
from mainapp import models as mainapp_models
from mainapp.forms import CourseFeedBackForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageView(ListView):
    model = News
    template_name = "mainapp/news_list.html"
    paginate_by = 2

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


class CoursesListView(ListView):
    model = Courses
    paginate_by = 5


class CoursesDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super(CoursesDetailView, self).get_context_data(**kwargs)
        context["course_object"] = get_object_or_404(mainapp_models.Courses, pk=pk)
        context["lessons"] = mainapp_models.Lesson.objects.filter(course=context["course_object"])
        context["teachers"] = mainapp_models.CourseTeachers.objects.filter(course=context["course_object"])
        context["feedback_list"] = mainapp_models.CourseFeedback.objects.filter(course=context["course_object"],
                                                                                deleted=False)
        is_commented = mainapp_models.CourseFeedback.objects.filter(
            course=context["course_object"],
            user=self.request.user,
            deleted=False
        ) != mainapp_models.CourseFeedback.objects.none()

        if self.request.user.is_authenticated and (not is_commented):
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


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class LoginPageView(TemplateView):
    template_name = "authapp/login.html"
