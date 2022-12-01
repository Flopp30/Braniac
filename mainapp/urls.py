from django.urls import path

from mainapp import views
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path("", views.MainPageView.as_view(), name="main_page"),
    path("courses/", views.CoursesListView.as_view(), name="courses"),
    path(
        "courses/<int:pk>/",
        views.CoursesDetailView.as_view(),
        name="courses_detail",
    ),
    path("contacts/", views.ContactsPageView.as_view(), name="contacts"),
    path("doc_site/", views.DocSitePageView.as_view(), name="doc_site"),
    path("login/", views.LoginPageView.as_view(), name="login"),

    # News
    path("news/", views.NewsPageView.as_view(), name="news"),
    path("news/add/", views.NewsCreateView.as_view(), name="news_create"),
    path("news/<int:pk>/update/", views.NewsUpdateView.as_view(), name="news_update"),
    path("news/<int:pk>/delete/", views.NewsDeleteView.as_view(), name="news_delete"),
    path("news/<int:pk>/detail/", views.NewsDetailView.as_view(), name="news_detail"),

]