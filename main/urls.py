from django.urls import path
from main.views import show_main, create_product, show_xml, show_json, show_xml_by_id, show_json_by_id
from main.views import register
from main.views import login_user
from main.views import logout_user
from main.views import increment_amount, decrement_amount, delete_product, edit_product,\
get_product_json, add_product_ajax, ajax_delete

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'), 
    path('create-product', create_product, name='create_product'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('increment_amount/<int:id>', increment_amount, name='increment_amount'),
    path('decrement_amount/<int:id>', decrement_amount, name='decrement_amount'),
    path('delete/<int:id>', delete_product, name='delete_product'),
    path('edit-product/<int:id>', edit_product, name='edit_product'),
    path('get-product/', get_product_json, name='get_product_json'),
    path('create-product-ajax/', add_product_ajax, name='add_product_ajax'),
    path('ajax-delete/<int:id>', ajax_delete, name='ajax_delete'),
]