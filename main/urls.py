from django.urls import path,include
from main.views import show_main,create_mood_entry,show_xml,show_xml_by_id,register,login_user,logout_user,edit_mood,delete_mood,add_mood_entry_ajax,show_json,show_json_by_id,create_mood_flutter,logout

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('xml/', show_xml, name='show_xml'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('logout/', logout_user, name='logout'),
    path('create-mood-entry',create_mood_entry,name='create_mood_entry'),
    path('login/', login_user, name='login'),
    path('delete/<uuid:id>', delete_mood, name='delete_mood'),
    path('edit-mood/<uuid:id>', edit_mood, name='edit_mood'),
    path('create-mood-entry-ajax', add_mood_entry_ajax, name='add_mood_entry_ajax'),
    path('json/', show_json, name='show_json'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('auth/', include('authentication.urls')),
    path('create-flutter/', create_mood_flutter, name='create_mood_flutter'),
    path('logout/', logout, name='logout'),
]