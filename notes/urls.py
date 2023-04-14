from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:note_id>/', views.detail, name='details'),
    path('add_note', views.add_note, name='add note'),
    #path('add_note_doing', views.add_note, name='add note doing'),
    path('note_added', views.note_added, name='note added'),
    path('move_note', views.move_note, name='move note'),
    path('safe_description/<int:note_id>', views.safe_description, name='safe description'),
    path('start_day', views.start_day, name='start day'),
    path('end_day', views.end_day, name='end day'),
    path('clear_day', views.clear_day, name='clear day'),
]