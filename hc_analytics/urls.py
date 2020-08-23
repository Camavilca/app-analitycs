"""hc_analytics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers
from hc_analytics.api import views

router = routers.DefaultRouter()
# router.register(r"reclutamiento", views.get_job_score)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path(
        "selection/employments/best-dictionary",
        views.Employment.as_view({"post": "post_best_dictionary"}),
    ),
    path(
        "selection/employments/match-cvs",
        views.Employment.as_view({"post": "post_match_cvs"}),
    ),
    path("selection/cvs/score", views.CV.as_view()),
    path("selection/match/all", views.Match.as_view({"post": "post_match_all"})),
    path("selection/math/average", views.Match.as_view({"post": "post_match_average"})),
]
