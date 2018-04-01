from django.urls import path

from mm import views

app_name = 'mm'
urlpatterns = [
    # Top-page
    path('', views.population_list, name='index'),

    # Population
    path('population/', views.population_list, name='population_list'),    # Show
    path('population/add/', views.population_edit, name='population_add'), # Add
    path('population/edit/<int:population_id>/', views.population_edit, name='population_edit'),  # Edit
    path('population/confirm/<int:population_id>/', views.population_confirm, name='population_confirm'),     # Confirm
    path('population/del/<int:population_id>/', views.population_del, name='population_del'),     # Delete

    # Strain
    path('strain/', views.strain_list, name='strain_list'),    # Show
    path('strain/population_id=<int:population_id>/', views.strain_list, name='strain_list_subset'),    # Show
    path('strain/edit/strain_id=<int:strain_id>/', views.strain_edit, name='strain_edit'),  # Edit
    path('strain/confirm/strain_id=<int:strain_id>/', views.strain_confirm, name='strain_confirm'),     # Confirm
    path('strain/del/strain_id=<int:strain_id>/', views.strain_del, name='strain_del'),     # Delete

    # Marker
    path('marker/', views.marker_list, name='marker_list'),    # Show
    path('marker/population_id=<int:population_id>/', views.marker_list, name='marker_list_subset'),    # Show
    path('marker/edit/marker_id=<int:marker_id>/', views.marker_edit, name='marker_edit'),  # Edit
    path('marker/confirm/marker_id=<int:marker_id>/', views.marker_confirm, name='marker_confirm'),     # Confirm
    path('marker/del/marker_id=<int:marker_id>/', views.marker_del, name='marker_del'),     # Delete

    # MS Table
    path('mstable/', views.mstable_list, name='mstable_list'),    # Show
    path('mstable/population_id=<int:population_id>/', views.mstable_list, name='mstable_list_subset'),    # Show
    path('mstable/view/', views.mstable_view, name='mstable_view'),  # View
    path('mstable/edit/mstable_id=<int:mstable_id>/', views.mstable_edit, name='mstable_edit'),  # Edit

    # Dataset
    path('dataset/upload/population_id=<int:population_id>/', views.dataset_upload, name='dataset_upload'),  # Upload
    path('dataset/import/population_id=<int:population_id>/', views.dataset_import, name='dataset_import'),  # Import
    path('dataset/export/population_id=<int:population_id>/', views.dataset_export, name='dataset_export'),  # Download

    # MMFinder
    path('mmf/setting/population_id=<int:population_id>/', views.mmf_setting, name='mmf_setting'),  # Setting
    path('mmf/search/population_id=<int:population_id>/',  views.mmf_search,  name='mmf_search'),  # Search
]
