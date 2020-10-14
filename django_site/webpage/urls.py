from django.conf.urls import url, include
from webpage import views

app_name = "webpage"
urlpatterns = [
        url(r'index/', views.index, name="index"),
        url(r'motor/', views.motor, name="motor"),
        url(r'servo/', views.servo, name="servo"),
        url(r'slide/', views.slide, name="slide"),
        url(r"qr_index/", views.qr_index, name="qr_index"),
        url(r"create_qrcode/", views.create_qrcode, name="create_qrcode"),
        
        
        url(r"form/", views.scan_qr_result, name="qr_result"),
        url(r"form/api/verify/getImgChaptchaDTO", views.getImgChaptchaDTO, name="getImgChaptchaDTO"),
        
        
        url(r"video/", views.video_feed, name="video"),
        url(r"map/", views.maps, name="map"),
        ]
