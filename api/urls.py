from django.urls import path
from .views import (RegisterAPI, LoginAPI, 
                    UserList, UserDetail,
                     CreateStaffUserAPI,
                    CustomerTransactionList,
                    CustomerTransactionDetail,
                    OwnTransactions, ChangeCustomerProfile)
from knox import views as knox_views



urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('create_staff_user/', CreateStaffUserAPI.as_view(), name='create_staff_user'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('users/', UserList.as_view()),
    path('delete_update_user/<int:pk>/', UserDetail.as_view()),
    path('update', ChangeCustomerProfile.as_view(), name='change_customer_profile_details'),
    path('transactions/', CustomerTransactionList.as_view(), name='get_list_of_all_transactions'),
    path('transaction/<int:pk>/', CustomerTransactionDetail.as_view(), name='get_a_transaction_detail'),
    path('own_products/',OwnTransactions.as_view(), name='Owntransactions'
    ),
    
]