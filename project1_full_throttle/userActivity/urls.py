from django.urls import path


from userActivity import views


urlpatterns = [
path('', views.home),
path('user_details', views.calculate_response_for_user)

]