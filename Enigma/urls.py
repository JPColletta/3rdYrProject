from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^presets/$', views.preset_list),
    url(r'^presets/(?P<pk>[0-9]+)$', views.preset_detail),

    url(r'^rotors/$', views.rotor_list),
    url(r'^rotors/(?P<pk>[0-9]+)$', views.rotor_detail),

    url(r'^reflectors/$', views.reflector_list),
    url(r'^reflectors/(?P<pk>[0-9]+)$', views.reflector_detail),
]
