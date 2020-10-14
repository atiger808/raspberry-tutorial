from django.conf.urls import url, include
from qrcode_detect import views

app_name  = 'qrcode_detect'

urlpatterns = [
    url(r'qr_index/', views.qr_index, name='qr_index'),
    url(r"qr_no_icon/", views.qrcode_no_icon, name="qr_no_icon"),
    url(r'qr_with_icon/', views.qrcode_with_icon, name='qr_with_icon'),
    url(r'upload_file/', views.upload_file, name='upload_file'),
    
    url(r"pic/", views.pic_show, name="pic_show"),
]