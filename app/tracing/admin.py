from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "name", "username", "telephone_number")


@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ("category_title",)


@admin.register(WorkStatus)
class WorkStatus(admin.ModelAdmin):
    list_display = ("pk", "status_title",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("location_title",)


class NonConformanceResource(resources.ModelResource):
    location = Field(column_name='location',
                     attribute='location',
                     widget=ForeignKeyWidget(Location, 'location_title')
                     )
    status = Field(column_name='status',
                               attribute='status',
                               widget=ForeignKeyWidget(WorkStatus, 'status_title')
                   )

    equipment = Field(column_name='equipment',
                      attribute='equipment',
                      widget=ForeignKeyWidget(Equipment, 'equipment_title')
                      )

    class Meta:
        model = NonConformance
        export_order = ("id", "created_at", "updated_at", "priority", "location", "status", "creator", "equipment",
                        "nc_description", "photo", "video",	"spare_parts", "moderator_comments", "tasks", "tasks_processed")


class NonConformanceInline(admin.TabularInline):
    model = NonConformance.spare_parts.through


@admin.register(NonConformance)
class NonConformanceAdmin(ImportExportModelAdmin):
    resource_class = NonConformanceResource

    inlines = (NonConformanceInline,)

    def get_inline_instances(self, request, obj=None):
        return [inline(self.model, self.admin_site) for inline in self.inlines]

    list_display = ("pk", "created_at", "priority", "equipment", "status", "nc_description", "creator")
    list_display_links = ("equipment",)
    list_filter = ("created_at", "priority", "status",)
    list_editable = ("status",)
    search_fields = ("equipment__equipment_title",)
    exclude = ("spare_parts",)
    readonly_fields = ("updated_at", "photo", "video", "priority", "tasks", "location",
                       "equipment", "creator")
    fields = ("updated_at", "priority", "location", "equipment",
              "status", "creator", "nc_description", "tasks", "tasks_processed",
              "moderator_comments", "photo", "video",)
    # save_as = True


class SparePartsInline(admin.TabularInline):
    model = SpareParts.equipment.through


@admin.register(SpareParts)
class SparePartsAdmin(admin.ModelAdmin):
    inlines = (SparePartsInline,)

    def get_inline_instances(self, request, obj=None):
        return [inline(self.model, self.admin_site) for inline in self.inlines]

    list_display = ("pk", "Assembly", "part_title", "manufacturer", "part_model",
                    "part_number", "equipment_quantity", "store_quantity")
    # list_display_links = ("nc_id", "created_at")
    list_editable = ("store_quantity",)
    list_filter = ("Assembly",)
    exclude = ("equipment",)


class EquipmentResource(resources.ModelResource):
    equipment_location = Field(column_name='equipment_location',
                               attribute='equipment_location',
                               widget=ForeignKeyWidget(Location, 'location_title')
                               )
    equipment_category = Field(column_name='equipment_category',
                               attribute='equipment_category',
                               widget=ForeignKeyWidget(EquipmentCategory, 'category_title')
                               )

    class Meta:
        model = Equipment
        export_order = ('id', 'equipment_full_title', 'equipment_title', 'inventory_number',
                        'equipment_location', 'area', 'equipment_category', 'priority_group')


@admin.register(Equipment)
class EquipmentAdmin(ImportExportModelAdmin):
    resource_class = EquipmentResource

    class Meta:
        model = Equipment

    list_display = ("priority_group", "equipment_title", "area", "equipment_category",)
    list_filter = ("priority_group", "equipment_location")
    list_display_links = ("equipment_title",)


# @admin.register(Equipment)
# class EquipmentAdmin(admin.ModelAdmin):
#     list_display = ("priority_group", "equipment_title", "area", "equipment_category", )
#     list_filter = ("priority_group", "equipment_location")
#     list_display_links = ("equipment_title",)


@admin.register(AssemblyGroup)
class AssemblyGroupAdmin(admin.ModelAdmin):
    list_display = ("group_title",)


class UsersInline(admin.TabularInline):
    model = Task.users.through


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = (UsersInline, )

    def get_inline_instances(self, request, obj=None):
        return [inline(self.model, self.admin_site) for inline in self.inlines]

    list_display = ("pk", "nc_id", "created_at", "work_status", )
    readonly_fields = ("photo", "video",)
    exclude = ("users",)
    fields = ("nc_id", "work_description", "work_status", "photo", "video", "comments", "used_parts")
    list_editable = ("work_status",)
    list_filter = ("created_at", "work_status",)


admin.site.site_title = "Управление несоответствиями"
admin.site.site_header = "Управление несоответствиями"
