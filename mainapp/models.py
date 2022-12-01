from django.db import models

NULLABLE = {'blank': True, 'null': True}


class MyCustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class BaseModel(models.Model):
    # objects = MyCustomManager()
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен", editable=False)

    deleted = models.BooleanField(default=False, verbose_name='Удален')

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        abstract = True


class News(BaseModel):
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    preambule = models.CharField(max_length=1024, verbose_name='Короткое описание')

    body = models.TextField(**NULLABLE, verbose_name='Тело новости')
    body_as_markdown = models.BooleanField(
        default=False, verbose_name='As markdown'
    )

    def __str__(self):
        return f'{self.pk} {self.title}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Courses(BaseModel):
    name = models.CharField(max_length=256, verbose_name="Имя")

    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    description_as_markdown = models.BooleanField(verbose_name="As markdown", default=False)

    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена", default=0)
    cover = models.CharField(max_length=25, default="no_image.svg", verbose_name="Лого")

    def __str__(self) -> str:
        return f"{self.pk} {self.name}"

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(BaseModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name='Название курса')
    num = models.PositiveIntegerField(verbose_name="Номер урока")

    title = models.CharField(max_length=256, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    description_as_markdown = models.BooleanField(verbose_name="As markdown", default=False)

    def __str__(self) -> str:
        return f"{self.course.name} | {self.num} | {self.title}"

    class Meta:
        ordering = ("course", "num")
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class CourseTeachers(models.Model):
    course = models.ManyToManyField(Courses)

    name_first = models.CharField(max_length=128, verbose_name="Имя")
    name_second = models.CharField(max_length=128, verbose_name="Фамилия")

    day_birth = models.DateField(verbose_name="Дата рождения")
    deleted = models.BooleanField(default=False, verbose_name='Удален')

    def __str__(self) -> str:
        return "{0:0>3} {1} {2}".format(self.pk, self.name_second, self.name_first)

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
