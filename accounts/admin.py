from django.contrib import admin
from django.utils.html import escape, mark_safe
from .models import Profile
from django.conf.urls import url
from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin import AdminSite
from blog.models import Article
from listings.models import Listing,ListingRating,ListingComment,ListingBooking
from django.db.models import Count
from django.views.generic import View
from django.template.loader import get_template 
from accounts.utils import render_to_pdf

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["profile_name", "email_confirmed",
                    "phone_number", "address", "user_email", "profile_pic", "active"]
    search_fields = ('user__username', 'phone_number', 'user_email',)
    list_filter = ['phone_number', 'user__email']
    list_editable = ['active', 'email_confirmed']
    list_per_page = 20

    def profile_name(self, obj):
        return obj.user.username

    def user_email(self, obj):
        return obj.user.email


admin.site.register(Profile, ProfileAdmin)

class MyAdminSite(AdminSite):

     def get_urls(self):
         from django.urls import path
         urls = super().get_urls()
         urls += [
             path('my_view/', self.admin_view(self.my_view))
         ]
         return urls

     def my_view(self, request):
        context = {}
        if request.method=="POST":
            fromdate=request.POST.get('fromdate')
            todate=request.POST.get('todate')
            request.session['firstdate'] = fromdate
            request.session['lastdate'] = todate

            total_user = Profile.objects.count()
            total_blog = Article.objects.filter(created_at__range=(fromdate, todate)).count()
            total_listing = Listing.objects.filter(created_at__range=(fromdate, todate)).count()
            total_booking = ListingBooking.objects.filter(created_at__range=(fromdate, todate)).count()
            total_comment = ListingComment.objects.filter(created_at__range=(fromdate, todate)).count()
            total_rating = ListingRating.objects.filter(created_at__range=(fromdate, todate)).count()


            context ={
            "total_user":total_user,
            "total_blog":total_blog,
            "total_listing":total_listing,
            "total_booking":total_booking,
            "total_comment":total_comment,
            "total_rating":total_rating,
            "fromdate":fromdate,
            "todate":todate,

            }

        return render(request, 'adminlte/report.html', context)
        #return HttpResponse("Hello!")
        

class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('adminlte/pdf/report.html')

        fromdate = request.session.get('firstdate')
        todate = request.session.get('lastdate')


        total_user = Profile.objects.count()
        total_blog = Article.objects.filter(created_at__range=(fromdate, todate)).count()
        total_listing = Listing.objects.filter(created_at__range=(fromdate, todate)).count()
        total_booking = ListingBooking.objects.filter(created_at__range=(fromdate, todate)).count()
        total_comment = ListingComment.objects.filter(created_at__range=(fromdate, todate)).count()
        total_rating = ListingRating.objects.filter(created_at__range=(fromdate, todate)).count()

        context ={
            "total_user":total_user,
            "total_blog":total_blog,
            "total_listing":total_listing,
            "total_booking":total_booking,
            "total_comment":total_comment,
            "total_rating":total_rating,
            "fromdate":fromdate,
            "todate":todate,

            }

        html = template.render(context)
        pdf = render_to_pdf('adminlte/pdf/report.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "report_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

admin_site = MyAdminSite()
generate_pdf = GeneratePDF()

