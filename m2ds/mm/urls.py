from django.urls import path
from mm import views

app_name = 'mm'
urlpatterns = [
    # URLs for Cultivation
    path('cult/', views.cult_list, name='cult_list'),    # Show
    path('cult/add/', views.cult_edit, name='cult_add'), # Add
    path('cult/edit/<int:cult_id>/', views.cult_edit, name='cult_edit'),  # Edit
    path('cult/del/<int:cult_id>/', views.cult_del, name='cult_del'),     # Delete

    # URLs for Strain
    path('strain/', views.strain_list, name='strain_list'),    # Show
#    path('strain/add/', views.strain_edit, name='strain_add'), # Add
#    path('strain/edit/<int:strain_id>/', views.strain_edit, name='strain_edit'),  # Edit
#    path('strain/del/<int:strain_id>/', views.strain_del, name='strain_del'),     # Delete
]
