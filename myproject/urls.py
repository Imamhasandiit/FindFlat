
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
from accounts.admin import admin_site
from accounts.admin import GeneratePDF
from accounts import views

urlpatterns = [
     path('admin/', admin.site.urls),
     path('admin/', admin_site.urls),
     path('accounts/', include('accounts.urls', namespace="accounts")),
     path('blog/', include('blog.urls', namespace="blog")),
     path('', include('listings.urls', namespace="listings")),

     path('admin/reports/pdf', GeneratePDF.as_view(), name='pdf_reports'),

     path('password_reset/', auth_views.PasswordResetView.as_view(),
          name='password_reset'),
     path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
          name='password_reset_done'),
     path('reset/<uidb64>/<token>',
          auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
          name='password_reset_complete'),
     path('logout/', views.logout_view, name='logout_view'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.FORCE_STATIC_FILE_SERVING and not settings.DEBUG:
    settings.DEBUG = True
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    settings.DEBUG = False


admin.site.site_header = "Finder Admin"
admin.site.site_title = "Finder Admin Portal"
admin.site.index_title = "Welcome to Find flat Near You"
