from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

    user_id = models.BigAutoField(unique=True, verbose_name="ID пользователя", primary_key=True)
    name = models.CharField(max_length=30, verbose_name="Имя пользователя")
    username = models.CharField(max_length=30, verbose_name="Никнейм пользователя", null=True, unique=True)
    telephone_number = models.PositiveIntegerField(verbose_name="Номер телефона", null=True, blank=True)

    def __str__(self):
        return self.name


class WorkStatus(models.Model):
    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    STATUS_SET = [
        ('создано', 'создано'),
        ('назначено', 'назначено'),
        ('остановлен', 'остановлен'),
        ('не подтверждено', 'не подтверждено'),
        ('не назначено', 'не назначено'),
        ('в процессе', 'в процессе'),
        ('требуется диагностика', 'требуется диагностика'),
        ('функциональность обеспечена', 'функциональность обеспечена'),
        ('требуется инструмент', 'требуется инструмент'),
        ('требуется материал', 'требуется материал'),
        ('выполнено', 'выполнено')
    ]

    status_title = models.CharField(max_length=30, choices=STATUS_SET, verbose_name="Статус работы", unique=True)

    def __str__(self):
        return self.status_title


class Location(models.Model):
    class Meta:
        verbose_name = "Расположение"
        verbose_name_plural = verbose_name

    location_title = models.CharField(max_length=20, verbose_name="Расположение",  unique=True)

    def __str__(self):
        return self.location_title


class EquipmentCategory(models.Model):
    class Meta:
        verbose_name = "Категория оборудования"
        verbose_name_plural = verbose_name

    category_title = models.CharField(max_length=30, verbose_name="Категория оборудования",  unique=True)

    def __str__(self):
        return self.category_title


class Equipment(models.Model):
    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = verbose_name

    equipment_title = models.CharField(max_length=35, verbose_name="Короткое название оборудования")
    equipment_full_title = models.CharField(max_length=100, verbose_name="Полное название оборудования",
                                            null=True, blank=True, unique=True)
    inventory_number = models.CharField(max_length=30, verbose_name="Инвентарный номер", null=True, blank=True)
    equipment_location = models.ForeignKey(Location, on_delete=models.PROTECT, verbose_name="Локация")
    area = models.CharField(max_length=100, verbose_name="Расположение", null=True, blank=True)
    equipment_category = models.ForeignKey(EquipmentCategory, on_delete=models.PROTECT,
                                           verbose_name="Категория оборудования")
    PRIORITY_GROUP = [
        ("A", 'A'),
        ("B", 'B'),
        ("C", 'C'),
    ]
    priority_group = models.CharField(max_length=20, choices=PRIORITY_GROUP, verbose_name="Группа критичности")

    def __str__(self):
        return self.equipment_title


class AssemblyGroup(models.Model):
    class Meta:
        verbose_name = "Техническая система"
        verbose_name_plural = "Технические системы"
    group_title = models.CharField(max_length=50, verbose_name="Производитель")

    def __str__(self):
        return self.group_title


class SpareParts(models.Model):
    class Meta:
        verbose_name = "Запасные части"
        verbose_name_plural = verbose_name
    equipment = models.ManyToManyField(Equipment, blank=True, verbose_name="Оборудование")
    Assembly = models.ForeignKey(AssemblyGroup, models.SET_NULL, blank=True,
                                 null=True, verbose_name="Техническая система")
    part_title = models.CharField(max_length=50, verbose_name="Название")
    manufacturer = models.CharField(max_length=50, verbose_name="Производитель", null=True, blank=True)
    part_model = models.CharField(max_length=50, verbose_name="Марка/Модель", null=True, blank=True)
    part_number = models.IntegerField(verbose_name="Каталожный номер", null=True, blank=True)
    equipment_quantity = models.PositiveIntegerField(verbose_name="К-во на оборудовании")
    store_quantity = models.PositiveIntegerField(verbose_name="К-во на складе")
    part_description = models.TextField(max_length=500, verbose_name="Описание Зап Части", null=True, blank=True)
    photo = models.CharField(max_length=200, blank=True, verbose_name="Фото", null=True)

    def __str__(self):
        return f"{self.part_title} {self.part_model} "


class NonConformance(models.Model):
    class Meta:
        verbose_name = "Несоответствие"
        verbose_name_plural = "Несоответствия"

    PRIORITY_GROUP = [
        ("A", 'A'),
        ("B", 'B'),
        ("C", 'C'),
    ]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создание записи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновление записи")
    location = models.ForeignKey(Location, models.PROTECT, verbose_name="Локация")
    priority = models.CharField(max_length=30, choices=PRIORITY_GROUP, verbose_name="Группа")
    creator = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, verbose_name="Создал")
    equipment = models.ForeignKey(Equipment, models.PROTECT, verbose_name="Оборудование")
    status = models.ForeignKey(WorkStatus, models.SET_NULL, verbose_name="Статус НС", blank=True, null=True,
                               default=1)
    nc_description = models.TextField(max_length=500, verbose_name="Описание НС")
    photo = models.CharField(max_length=200, blank=True, verbose_name="Фото", null=True)
    video = models.CharField(max_length=200, blank=True, verbose_name="Видео", null=True)
    spare_parts = models.ManyToManyField(SpareParts, blank=True, verbose_name="Использовали зап части")
    moderator_comments = models.TextField(max_length=1000, verbose_name="Примечание модератора", null=True, blank=True)
    tasks = models.PositiveSmallIntegerField(verbose_name="Количество назначенных задач", blank=True, null=True)
    tasks_processed = models.PositiveSmallIntegerField(verbose_name="Количество обработанных задач",
                                                       blank=True, null=True)

    def __str__(self):
        return str(self.pk)


class Task(models.Model):
    class Meta:
        verbose_name = "Задача(у)"
        verbose_name_plural = "Задачи"

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания задачи")
    users = models.ManyToManyField(User, blank=True, verbose_name="Исполнитель(и)")
    used_parts = models.ManyToManyField(SpareParts, blank=True, verbose_name="Использовали зап части")
    nc_id = models.ForeignKey(NonConformance, on_delete=models.PROTECT, verbose_name="ID несоответствия",)
    work_status = models.ForeignKey(WorkStatus, models.SET_NULL, verbose_name="Статус НС", blank=True, null=True)
    work_description = models.TextField(max_length=500, verbose_name="Что сделано", blank=True, null=True)
    comments = models.CharField(max_length=254, blank=True, verbose_name="Примечание модератора")
    photo = models.CharField(max_length=200, blank=True, verbose_name="Фото", null=True)
    video = models.CharField(max_length=200, blank=True, verbose_name="Видео", null=True)

    def __str__(self):
        return f"{self.pk}"
