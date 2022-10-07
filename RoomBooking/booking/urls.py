from rest_framework.routers import SimpleRouter
from api import views
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path


router = SimpleRouter()

router.register(r'api/room',
                views.RoomViewSet, 'Room')
router.register(r'api/event',
                views.EventViewSet, 'Event')
router.register(r'api/booking',
                views.BookingViewSet, 'Booking')

urlpatterns = router.urls
urlpatterns += [
    path('api-token-auth/', obtain_auth_token,
         name='api_token_auth'),
]
