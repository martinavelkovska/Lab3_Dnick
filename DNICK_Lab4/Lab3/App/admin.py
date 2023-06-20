from django.contrib import admin
from .models import Avtor, Komentar, Post, Blok
from django.core.exceptions import PermissionDenied
# Register your models here.

class AvtorAdmin(admin.ModelAdmin):
    list_display = ("ime", "prezime")
    exclude = ("user",)


    def has_change_permission(self, request, obj=None):
        if obj and (request.user == obj.user):
            return True
        else:
            return False

    def has_view_permission(self, request, obj=None) -> bool:
        return True

    def has_delete_permission(self, request, obj=None):
        if (obj and (request.user == obj.user)) or request.user.is_superuser:
            return True
        else:
            return False

    def has_add_permission(self, request, obj=None):
        return True

    def save_model(self, request, obj, form, change):
        if obj is not None:
            obj.user = request.user

        super().save_model(request, obj, form, change)


class PostAdmin(admin.ModelAdmin):
    list_display = ("naslov", "avtor",)
    search_fields = ("naslov", "sodrzina",)
    list_filter = ("datum_created",)
    exclude = ("avtor",)

    def has_view_permission(self, request, obj=None) -> bool:
        if obj is not None:
            if request.user.is_superuser:
                return True
            if obj.blocked_users.filter(id=request.user.id).exists():
                raise PermissionDenied("You are not allowed to view this post.")
                return False
        return True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            blocked = Blok.objects.filter(blokiran__user=request.user).values_list('bloker__user', flat=True)
            qs = qs.exclude(avtor__user__in=blocked)
        return qs

    def has_change_permission(self, request, obj=None):
        if (obj and request.user == obj.avtor.user) or request.user.is_superuser:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if (obj and request.user == obj.avtor.user ) or request.user.is_superuser:
            return True
        else:
            return False

    def has_add_permission(self, request, obj=None) -> bool:
        return True

    def save_model(self, request, obj, form, change):
        if obj is not None:
            if request.user.is_superuser:
                obj.avtor = Avtor.objects.get(user=request.user)
            else:
                obj.avtor = Avtor.objects.get(user=request.user)


        super().save_model(request, obj, form, change)
admin.site.register(Post, PostAdmin)

class KomentarAdmin(admin.ModelAdmin):
    list_display = ("sodrzina", "datum_created" ,"user")
    exclude = ("user",)

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or (obj and Blok.objects.filter(bloker__user=obj.post.avtor.user).exists()) or request.user

    def has_delete_permission(self, request, obj=None):
        if obj and (request.user == obj.user.user or request.user == obj.post.avtor.user or request.user.is_superuser):
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if(obj and request.user == obj.user.user) or request.user.is_superuser:
            return True
        else:
            return False


    def has_add_permission(self, request) -> bool:
        return True


    def save_model(self, request, obj, form, change):
        if obj is not None:
            if request.user.is_superuser:
                obj.user = Avtor.objects.get(user=request.user)
            else:
                obj.user = Avtor.objects.get(user=request.user)

        super().save_model(request, obj, form, change)

class BlokAdmin(admin.ModelAdmin):
     exclude = ("bloker",)

     def has_view_permission(self, request, obj=None):
        if obj and (request.user == obj.bloker.user or request.user.is_superuser):
            return True
        return False

     def has_change_permission(self, request, obj=None):
        if obj and (request.user == obj.bloker.user or request.user.is_superuser):
            return True
        return False

     def has_add_permission(self, request,  obj=None):
        return True

     def has_delete_permission(self, request, obj=None):
        if obj and (request.user == obj.bloker.user or request.user.is_superuser):
            return True
        return False

     def save_model(self, request, obj, form, change):
        if obj is not None:
             if request.user.is_superuser:
                obj.bloker = Avtor.objects.get(user=request.user)
             else:
                obj.bloker = Avtor.objects.get(user=request.user)

        super().save_model(request, obj, form, change)


admin.site.register(Avtor, AvtorAdmin)

admin.site.register(Komentar, KomentarAdmin)

admin.site.register(Blok, BlokAdmin)
