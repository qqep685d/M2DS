from django.urls import path

from mm import views

app_name = 'mm'
urlpatterns = [
    # Top-page
    path('', views.index, name='index'),

    # Population
    path('population/', views.population_list, name='population_list'),    # Show
    path('population/add/', views.population_edit, name='population_add'), # Add
    path('population/edit/<int:population_id>/', views.population_edit, name='population_edit'),  # Edit
    path('population/confirm/<int:population_id>/', views.population_confirm, name='population_confirm'),     # Delete
    path('population/del/<int:population_id>/', views.population_del, name='population_del'),     # Delete

    # Dataset
    path('dataset/upload/<int:population_id>/', views.dataset_upload, name='dataset_upload'),  # Upload
    path('dataset/import/<int:population_id>/', views.dataset_import, name='dataset_import'),  # Import

    # Strain
    path('strain/', views.strain_list, name='strain_list'),    # Show
    path('strain/pop=<int:population_id>', views.strain_list, name='strain_list_subset'),    # Show
    path('strain/?population_id=<int:population_id>', views.strain_list, name='strain_list_get'),    # Show
#    path('strain/add/', views.strain_edit, name='strain_add'), # Add
#    path('strain/edit/<int:strain_id>/', views.strain_edit, name='strain_edit'),  # Edit
#    path('strain/del/<int:strain_id>/', views.strain_del, name='strain_del'),     # Delete

    # Marker
    path('marker/', views.marker_list, name='marker_list'),    # Show
    path('marker/pop=<int:population_id>', views.marker_list, name='marker_list_subset'),    # Show

    # MS Table
    path('mstable/', views.mstable_list, name='mstable_list'),    # Show
    path('mstable/pop=<int:population_id>', views.mstable_list, name='mstable_list_subset'),    # Show
]
