from django.contrib import admin
from .models import Work, ArtistProfile, Certification

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')

admin.site.register(ArtistProfile)
admin.site.register(Certification)
