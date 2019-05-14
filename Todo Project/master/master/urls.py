from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings


admin.site.site_header = "Todo BackOffice"
admin.site.site_title = "Todo Admin Portal"
admin.site.index_title = "Welcome to Todo Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),
    path('user/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
