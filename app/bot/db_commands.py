from tracing.models import *
from asgiref.sync import sync_to_async
from django.db.models import F


@sync_to_async
def select_user(user_id: int):
    """Выбрать пользователя"""
    return User.objects.filter(user_id=user_id).first()


@sync_to_async
def user_create(user_id, name, username):
    """Добавить пользователя"""
    return User(user_id=int(user_id), name=name, username=username).save()


@sync_to_async
def get_user(user_id):
    users = User.objects.get(user_id=user_id)
    return users


@sync_to_async
def select_location():
    """Выбрать локацию"""
    return Location.objects.all()


@sync_to_async
def select_non_conformance(pk):
    """Выбрать несоответствие по ключу"""
    return NonConformance.objects.get(pk=pk)


@sync_to_async
def select_equip_category(location, priority):
    """Выбрать категорию оборудования"""
    return Equipment.objects.filter(priority_group=priority).filter(equipment_location=location).distinct("equipment_category")


@sync_to_async
def select_priority(location):
    """Выбрать группу критичности"""
    return Equipment.objects.filter(equipment_location=location).distinct("priority_group")


@sync_to_async
def select_equipments(location, priority, equip_category):
    """Выбрать категорию локаций поезда, с группой критичности и категорией оборудования"""
    return Equipment.objects.filter(equipment_location=location) \
        .filter(priority_group=priority) \
        .filter(equipment_category=equip_category)


@sync_to_async
def create_non_conformance(user, location, priority, equipment_id, description, photo_id, video_id):
    """Записать новое несоответствие в базу данных"""
    creator = User.objects.get(user_id=user)
    equipment = Equipment.objects.get(pk=equipment_id)
    location = Location.objects.get(pk=location)
    status = WorkStatus.objects.get(pk=1)
    new_non_conformance = NonConformance(creator=creator,
                                         priority=priority,
                                         nc_description=description,
                                         equipment=equipment,
                                         photo=photo_id,
                                         video=video_id,
                                         location=location,
                                         status=status,
                                         )
    new_non_conformance.save()
    return new_non_conformance


@sync_to_async
def get_equipment_title(equipment_id):
    """Получаем имя оборудования"""
    return Equipment.objects.get(pk=equipment_id)


@sync_to_async
def get_my_nc():
    """Получить только несоответствия c указанным статусом"""
    status_list = ['не назначено', 'в процессе', 'требуется диагностика', 'функциональность обеспечена',
                   'требуется инструмент', 'требуется материал',]
    list_nc = NonConformance.objects.filter(status__status_title__in=status_list).order_by('status')
    res = []
    if list_nc:
        for x in list_nc:
            res.append(x)
        return res
    else:
        return


@sync_to_async
def fetch_media(id: int):
    """Получаем медиафайл по ID несоответствия"""
    try:
        get_nc = NonConformance.objects.get(pk=id)
        if get_nc.photo:
            media = get_nc
        else:
            media = get_nc
        return media
    except:
        return None


@sync_to_async
def get_tasks(user_id):
    """Получаем статус задачи с фильтрами по user_id"""
    # status_list = ['создано', 'не назначено', 'не подтверждено', 'остановлен', 'завершен', ]
    # tasks = Task.objects.filter(users__user_id=user_id).exclude(work_status__status_title__in=status_list)
    status = 'назначено'
    tasks = Task.objects.filter(users__user_id=user_id).filter(work_status__status_title=status)
    return tasks


@sync_to_async
def get_nc_4_tasks(pk):
    """ Получить  несоответствия по Private key"""
    queryset = NonConformance.objects.get(pk=pk)
    if NonConformance.objects.get(pk=pk):
        return queryset
    else:
        return


@sync_to_async
def get_task_status():
    """Получаем статус с исключением из списка"""
    status_list = ['создано', 'не назначено', 'не подтверждено', 'остановлен', 'назначено']
    return WorkStatus.objects.exclude(status_title__in=status_list)


@sync_to_async
def write_task_report(task_pk, nc_id, description, work_status, photo_id, video_id):
    """Записать отчет по задаче"""
    status = WorkStatus.objects.get(pk=work_status)
    new_report_task = Task.objects.filter(pk=task_pk)\
                                  .update(work_description=description,
                                          work_status=status,
                                          photo=photo_id,
                                          video=video_id,
                                          )
    #
    NonConformance.objects.filter(pk=nc_id).update(tasks_processed=F("tasks_processed") + 1)
    return new_report_task


@sync_to_async
def task_count(nc_id):
    """Подсчитать количество задач"""
    count = Task.objects.filter(nc_id=nc_id).count()
    return NonConformance.objects.filter(pk=nc_id).update(tasks=count)

# @sync_to_async
# def get_all_nc():
#     list = nc.objects.all()
#     return list
# @sync_to_async
# def get_nc(hours=11):
#     """Получить все несоответствия за последние 11 часов"""
#     now = timezone.now()
#     before = now - timedelta(hours=hours)
#     list_nc = nc.objects.filter(created_at__gte=before)
#     if list_nc:
#         res = []
#         for x in list_nc:
#             res.append(x)
#         return res
#     else:
#         return
#
#


#
@sync_to_async
def user_task_list(task_id):
    """Выбрать """
    task_value_list = Task.objects.filter(pk=task_id).values_list("users__name")
    user_list = []
    for i in task_value_list:
        user_list.append(i[0])
    join_result = ", ".join(map(str, user_list))
    return join_result


@sync_to_async
def get_equipment_area(title):
    """Получаем расположение оборудования"""
    q = Equipment.objects.get(equipment_title=title)
    return q.area


@sync_to_async
def get_task_status_title(status_id):
    """Получаем имя статуса"""
    q = WorkStatus.objects.get(pk=status_id)
    return q.status_title
