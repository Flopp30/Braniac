from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class MyCustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class BaseModel(models.Model):
    # objects = MyCustomManager()
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"), editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name=_("updated"), editable=False)

    deleted = models.BooleanField(default=False, verbose_name=_('deleted'))

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        abstract = True


class News(BaseModel):
    title = models.CharField(max_length=128, verbose_name=_('header'))
    preambule = models.CharField(max_length=1024, verbose_name=_('short description'))

    body = models.TextField(**NULLABLE, verbose_name=_('body'))
    body_as_markdown = models.BooleanField(
        default=False, verbose_name=_('As markdown')
    )

    def __str__(self):
        return f'{self.pk} {self.title}'

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')


class Courses(BaseModel):
    name = models.CharField(max_length=256, verbose_name=_("name"))

    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    description_as_markdown = models.BooleanField(verbose_name=_("As markdown"), default=False)

    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_("price"), default=0)
    cover = models.CharField(max_length=25, default="no_image.svg", verbose_name=_("logo"))

    def __str__(self) -> str:
        return f"{self.pk} {self.name}"

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')


class Lesson(BaseModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name=_('Course name'))
    num = models.PositiveIntegerField(verbose_name=_("lesson number"))

    title = models.CharField(max_length=256, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"), blank=True, null=True)
    description_as_markdown = models.BooleanField(verbose_name=_("As markdown"), default=False)

    def __str__(self) -> str:
        return f"{self.course.name} | {self.num} | {self.title}"

    class Meta:
        ordering = ("course", "num")
        verbose_name = _('lesson')
        verbose_name_plural = _('lessons')


class CourseTeachers(models.Model):
    course = models.ManyToManyField(Courses)

    name_first = models.CharField(max_length=128, verbose_name=_("first name"))
    name_second = models.CharField(max_length=128, verbose_name=_("last name"))

    day_birth = models.DateField(verbose_name=_("date birth"))
    deleted = models.BooleanField(default=False, verbose_name=_('Deleted'))

    def __str__(self) -> str:
        return "{0:0>3} {1} {2}".format(self.pk, self.name_second, self.name_first)

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = _('teacher')
        verbose_name_plural = _('teachers')


class CourseFeedback(BaseModel):

    RATINGS = (
        (5, '⭐⭐⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (3, '⭐⭐⭐'),
        (2, '⭐⭐'),
        (1, '⭐'),
    )
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name=_('Course'))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('User'))
    rating = models.SmallIntegerField(choices=RATINGS, default=5, verbose_name=_('rating'))
    feedback = models.TextField(default=_('Without a review'), verbose_name=_('feedback'))

    class Meta:
        verbose_name = _('feedback')
        verbose_name_plural = _('feedbacks')

    def __str__(self):
        return f'Отзыв на {self.course} от {self.user}'
