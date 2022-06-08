from django.contrib import admin
from .models import Profile
from .models import AuditEntry
from django.http import HttpResponse

# Register your models here.
admin.site.register(Profile)

# rejestrowanie informacji o logowaniu i wylogowaniu
@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    # informacje, które mają się wyświetlać w panelu administratora
    list_display = ['time', 'action', 'username', 'ip',]
    # dane, po których można filtrować (log/wylog)
    list_filter = ['action',]
    #list_display = ('time', 'username', 'action', 'ip')
    # określanie pól jako read-only - logów nie można edytować
    readonly_fields = ['time', 'username', 'action', 'ip']
    # utworzenie akcji do pobrania logów przez panel administratora
    actions = ["download_csv"]

    # funkcja do pobierania pliku .csv
    def download_csv(modeladmin, request, queryset):
        import csv
        from django.utils import dateformat

        # tworzenie zapytania http dla csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format('audit_logs')

        # rozpoczęcie wpisywania do csv
        writer = csv.writer(response)
        # nagłówki
        writer.writerow(['Date Time', 'Username', 'Action', 'IP Address'])
        # dla każdego logu wpisujemy go do csv
        for s in queryset:
            writer.writerow([dateformat.format(s.time, 'Y-m-d H:i:s'), s.username, s.action, s.ip])
        # zwracamy zapytanie - rozpoczyna się pobieranie
        return response
