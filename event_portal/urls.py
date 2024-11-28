from django.urls import path
from .views import *

urlpatterns = [
    
    # Category
    path('create_event_category/', CreateEventCategory.as_view(), name='create_event_category'),
    path('retrieve_event_category/', RetrieveEventCategory.as_view(), name='retrieve_event_category'),
    path('update_event_category/<int:category_id>/', UpdateEventCategory.as_view(), name='update_event_category'),
    
    # Event 
    path('create_event/', CreateEvent.as_view(), name='create_event'),
    path('retrieve_event/', RetrieveEvent.as_view(), name='retrieve_event'),
    path('update_event/<int:event_id>/', UpdateEvent.as_view(), name='update_event'),
    path('inactive_event/<int:event_id>/', DeactivateEvent.as_view(), name='inactive_event'),
    path('active_event/', ActiveEvent.as_view(), name='active_event'),
    path('event_by_category/<int:category_id>/', EventByCategory.as_view(), name='event_by_category'),
    

]
