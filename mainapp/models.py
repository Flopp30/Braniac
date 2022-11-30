from django.db import models

NULLABLE = {'blank': True, 'null': True}


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Edited", editable=False)

    deleted = models.BooleanField(default=False)

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        abstract = True


class News(BaseModel):
    title = models.CharField(max_length=128, verbose_name='Title')
    preambule = models.CharField(max_length=1024, verbose_name='Preambule')

    body = models.TextField(**NULLABLE, verbose_name='Body')
    body_as_markdown = models.BooleanField(
        default=False, verbose_name='As markdown'
    )

    def __str__(self):
        return f'{self.pk} {self.title}'


class CoursesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class Courses(BaseModel):
    objects = CoursesManager()

    name = models.CharField(max_length=256, verbose_name="Name")

    description = models.TextField(verbose_name="Description", blank=True, null=True)
    description_as_markdown = models.BooleanField(verbose_name="As markdown", default=False)

    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Cost", default=0)
    cover = models.CharField(max_length=25, default="no_image.svg", verbose_name="Cover")

    def __str__(self) -> str:
        return f"{self.pk} {self.name}"


class Lesson(BaseModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name="Lesson number")

    title = models.CharField(max_length=256, verbose_name="Name")
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    description_as_markdown = models.BooleanField(verbose_name="As markdown", default=False)

    def __str__(self) -> str:
        return f"{self.course.name} | {self.num} | {self.title}"

    class Meta:
        ordering = ("course", "num")


class CourseTeachers(models.Model):
    course = models.ManyToManyField(Courses)

    name_first = models.CharField(max_length=128, verbose_name="Name")
    name_second = models.CharField(max_length=128, verbose_name="Surname")

    day_birth = models.DateField(verbose_name="Birth date")
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "{0:0>3} {1} {2}".format(self.pk, self.name_second, self.name_first)

    def delete(self, *args):
        self.deleted = True
        self.save()