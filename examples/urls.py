from django.urls import path

from . import views

from .views import refresh


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('filter/', views.MyStockFilterView.as_view(), name='filter_mystock'),
    path('create/', views.MyStockCreateView.as_view(), name='create_mystock'),
    path('update/<int:pk>', views.MyStockUpdateView.as_view(), name='update_mystock'),
    path('read/<int:pk>', views.MyStockReadView.as_view(), name='read_mystock'),
    path('delete/<int:pk>', views.MyStockDeleteView.as_view(), name='delete_mystock'),
    path('mystocks/', views.mystocks, name='mystocks'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('refresh/', refresh, name='refresh'),
    path('population-chart/', views.population_chart, name='population-chart'),
    path('accumulate-chart/', views.accumulate_chart, name='accumulate-chart'),
    path('bubble-chart/', views.bubble_chart, name='bubble-chart'),
    path('pie-chart/', views.pie_chart, name='pie-chart'),
    path('kospi-chart/', views.kospi_chart, name='kospi-chart'),
    path('createbalances/', views.BalancesCreateView.as_view(), name='create_balances'),
    path('updatebalances/<int:pk>', views.BalancesUpdateView.as_view(), name='update_balances'),
    path('deletebalances/<int:pk>', views.BalancesDeleteView.as_view(), name='delete_balances'),
    path('balances/', views.balances, name='balances'),
    path('mixed-chart/', views.mixed_chart, name='mixed-chart'),
    
]


