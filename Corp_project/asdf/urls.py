from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index_Page, name = 'Index_Page'),
    
    path('signup/', views.Signup_Page, name = 'Signup_Page'),

    path('login/', views.Login_Page, name = 'Login_Page'),

    path('signup_action/', views.Signup_Action, name = 'Signup_Action'),

    path('login_action/', views.Login_Action, name = 'Login_Action'),

    path('logout/', views.Logout, name = 'Logout'),

    path('board/', views.Board_Page, name = 'Board_Page'),

    path('post_writing/', views.Post_Writing_Page, name = 'Post_Writing_Page'),

    path('post_writing_action/', views.Post_Writing_Action, name = 'Post_Writing_Action'),

    path('post_detail/<int:post_id>/', views.Post_Detail_Page, name = 'Post_Detail_Page'),

    path('myaccount/', views.Myaccount_Page, name = 'Myaccount_Page'),

    path('edit_info', views.Edit_Info, name = 'Edit_Info'),

    path('user_detail/<int:connected_user_id>/', views.User_Detail_Page, name = 'User_Detail_Page'),

    path('delete_post/<int:post_id>', views.Delete_Post, name = 'Delete_Post'),

    path('message_box/', views.Message_Box_Page, name = 'Message_Box_Page'),

    path('message_writing/', views.Message_Writing_Page, name = 'Message_Writing_Page'),

    path('message_writing_action/', views.Message_Writing_Action, name = 'Message_Writing_Action'),

    path('message_detail/<int:message_id>/', views.Message_Detail_Page, name = 'Message_Detail_Page'),

    path('message_reply/<int:connected_user_id>/', views.Message_Reply_Page, name = 'Message_Reply_Page'),

    path('message_delete/<int:message_id>/', views.Message_Delete, name = 'Message_Delete'),

    #ych
    path('challenge/', views.challenge_level_selection, name='challenge_level_selection'),
    path('battle/<int:level>/', views.battle_page, name='battle_page'),
    path('reset_battle/<int:level>/', views.reset_battle, name='reset_battle'),  # 전투 상태 초기화 URL
]
