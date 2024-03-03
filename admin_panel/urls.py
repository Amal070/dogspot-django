from django.urls import path

from admin_panel.views import *

urlpatterns = [
    path('dashboard/', dashboard, name='admin.dashboard'),
    path('map/', map, name='admin.map'),
    path('user/',users,name='admin.users'),
    path('user_details/<pk>',user_details,name='admin.user_details'),
    path('missings_a/',missings_all,name='admin.missings_all'),
    path('missing_details_a/<pk>',missing_details_all,name='admin.missing_details_all'),
    path('missings_y/',missings_your,name='admin.missings_your'),
    path('missing_details_y/<pk>',missing_details_your,name='admin.missing_details_your'),
    path('missings_form/',missings_form,name='admin.missings_form'),
    path('missing_edit/<pk>',edit,name='admin.missing_edit'),
    path('missing_delete_a/<pk>',delete_a,name='admin.missing_delete_a'),
    path('missing_delete_y/<pk>',delete_y,name='admin.missing_delete_y'),
    path('comment_a/<pk>',comment_a,name='admin.comment_a'),
    path('comment_y/<pk>',comment_y,name='admin.comment_y'),
    path('comment_delete_a/<pk>',comment_delete_all,name='admin.comment_delete_all'),
    path('comment_delete_y/<pk>',comment_delete_your,name='admin.comment_delete_your'),
    path('report_list/',report_list,name='admin.report_list'),
    path('report_delete_l/<pk>',report_delete_l,name='admin.report_delete_l'),
    path('report_case_a/<pk>',report_all,name='admin.report_all'),
    path('report_case_y/<pk>',report_your,name='admin.report_your'),
    path('report_delete_a/<pk>',report_delete_all,name='admin.report_delete_all'),
    path('report_delete_y/<pk>',report_delete_your,name='admin.report_delete_your'),
    path('profile/',profile,name='admin.profile'),
    path('profile_update/',profile_edit,name='admin.profile_edit'),
    path('adoption_form/',adoption_form,name='admin.adoption_form'),
    path('adoption/',adoption_view,name='admin.adoption_view'),
    path('adoption_edit/<pk>',edit_adoption,name='admin.edit_adoption'),
    path('adoption_detail/<pk>',adoption_details,name='admin.adoption_details'),
    path('adoption_delete/<pk>',adoption_delete,name='admin.adoption_delete'),
    path('adoption_all/',adoption_all_view,name='admin.adoption_all_view'),
    path('adoption_all_detail/<pk>',adoption_all_details,name='admin.adoption_all_details'),
    path('adoption_all_delete/<pk>',adoption_all_delete,name='admin.adoption_all_delete'),
    path('adoption_req_snd/',adoption_snd_view,name='admin.adoption_snd_view'),
    path('adp_request_list/<pk>', request_list,name='admin.request_list'),
    path('request_profile/<pk>', request_profile,name='admin.request_profile'),
    path('request_cancel/<pk>', request_cancel,name='admin.request_cancel'),
    path('request_send/<pk>', request_send,name='admin.request_send'),
]
