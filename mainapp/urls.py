from django.urls import path
from django.views.decorators.cache import cache_page
from mainapp import views
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path("", views.MainPageView.as_view(), name="main_page"),
    path("contacts/", views.ContactsPageView.as_view(), name="contacts"),
    path("doc_site/", views.DocSitePageView.as_view(), name="doc_site"),
    path("login/", views.LoginPageView.as_view(), name="login"),

    # Courses
    path("courses/", cache_page(300)(views.CoursesListView.as_view()), name="courses"),
    path("courses/<int:pk>/", views.CoursesDetailView.as_view(), name="courses_detail", ),
    path("courses/feedback/", views.CourseFeedbackCreateView.as_view(), name="course_feedback", ),

    # News
    path("news/", cache_page(300)(views.NewsPageView.as_view()), name="news"),
    path("news/add/", views.NewsCreateView.as_view(), name="news_create"),
    path("news/<int:pk>/update/", views.NewsUpdateView.as_view(), name="news_update"),
    path("news/<int:pk>/delete/", views.NewsDeleteView.as_view(), name="news_delete"),
    path("news/<int:pk>/detail/", views.NewsDetailView.as_view(), name="news_detail"),

    # Logs
    path("logs/", views.LogView.as_view(), name="log_list"),
    path("logs/download/", views.LogDownloadView.as_view(), name="log_download"),

]
