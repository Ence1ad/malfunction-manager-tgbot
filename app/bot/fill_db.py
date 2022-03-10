from tracing.models import Location, EquipmentCategory, WorkStatus, User
# admin = int(os.getenv("ADMIN_ID"))


def fill_db():
    """Для начальной загрузки бд через shall"""
    admin = User(user_id=1581059021, name="Вадим Литовченко")
    admin.save()
    location = ["Депо", "КМК", "ДОЛБ"]
    for i in location:
        var = Location(location_title=i)
        var.save()
    equipment_category = ["Внутрицеховой транспорт", "Ворота", "ГПМ", "Рабочие площадки", "Лестницы",
                          "Инженерные системы", "Путь 1,2", "Система подачи сжатого воздуха", "Очистное оборудование",
                          "Паяльники", "Подача напряжения", "Зарядные устройства", "Разное", "Станки", "Инж. Сист"]
    new_status = ['не назначено', 'в процессе', 'требуется диагностика', 'функциональность обеспечена',
                  'требуется инструмент', 'требуется материал', 'создано', 'не подтверждено', 'назначено', 'остановлен',
                  'завершен']
    for i in equipment_category:
        e = EquipmentCategory(category_title=i)
        e.save()
    for i in new_status:
        w = WorkStatus(status_title=i)
        w.save()
    return


