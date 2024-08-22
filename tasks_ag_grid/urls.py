from django.urls import path
from .views.tasks_ag_grid import tasks_grid

urlpatterns = [
    path("home/", tasks_grid, name='tasks_grid'),
]
