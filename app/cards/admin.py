from django.contrib import admin

from .models import Card, CardLink


class CardLinkInline(admin.TabularInline):
    model = CardLink
    extra = 1


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'company', 'updated_at')
    search_fields = ('user__email', 'user__slug', 'first_name', 'last_name')
    inlines = [CardLinkInline]
