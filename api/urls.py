from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


urlpatterns = [
    # Authentication
    path('signup', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('authentication-status', views.authentication_status, name='authentication-status'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('doctors', views.doctors_view, name='doctors'),
    path('inspectors', views.inspectors_view, name='inspectors'),
    path('patients', views.patients_view, name='patients'),

    path('doctor/<int:pk>', views.doctor_view, name='doctor'),
    path('inspector/<int:pk>', views.inspector_view, name='inspector'),
    path('patient/<int:pk>', views.patient_view, name='patient'),

    path('request/<int:pk>', views.request_by_id_view, name='request-by-id'),
    path('request', views.request_view, name='request'),
    path('requests', views.requests_view, name='requests'),
    path('accept-request', views.accept_request_view, name='accept-request'),
    path('reject-request', views.reject_request_view, name='reject-request'),
    path('request-visibility/<int:pk>', views.request_visibility_view, name='request-visibility'),
]
