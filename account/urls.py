from django.urls import path,include
from . import views


urlpatterns = [
    path("register/",views.registration,name="register"),
    path("logout/",views.user_logout,name="logout"),
    path("profile/",views.profile,name="profile"),
    path("login/",views.user_login,name="login"),
    path("activate/<uid>/<token>/",views.activate_user,name="activate_user"),
    path("profile_update/",views.profile_update,name="profile_update"),
    path("order_history/",views.order_history,name="order_history"),
    path("order_details/<int:id>",views.order_details,name="order_details"),
    path("track_order/<int:id>",views.track_order,name="track_order"),
    path("transactions/",views.transactions,name="transactions"),
    path("recieved/",views.recieved,name="recieved"),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    
    
    # path("check/",views.check,name="check"),
]
