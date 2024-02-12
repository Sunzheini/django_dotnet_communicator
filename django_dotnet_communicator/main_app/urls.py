from django.urls import path
from django_dotnet_communicator.main_app.views import index_view, post_view, get_view, edit_view, delete_view

"""
Postman:
Headers -> Content-Type -> application/json
Body -> raw -> JSON
{
    "name": "new item"
}
"""
urlpatterns = [
    # http://127.0.0.1:8000/
    path('', index_view, name='index'),

    # http://127.0.0.1:8000/post/
    path('post/', post_view, name='post'),

    # http://127.0.0.1:8000/get/1/
    path('get/<int:pk>/', get_view, name='get'),

    # http://127.0.0.1:8000/edit/1/
    path('edit/<int:pk>/', edit_view, name='edit'),

    # http://127.0.0.1:8000/delete/1/
    path('delete/<int:pk>/', delete_view, name='delete'),
]
