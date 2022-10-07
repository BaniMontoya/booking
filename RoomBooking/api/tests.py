from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api import models as booking_models


class TestCasebooking(APITestCase):

    def setup_user(self, name, email, is_bussines):
        self.User_obj = get_user_model()
        self.user = self.User_obj.objects.create_user(
            name,
            email=email,
            password='test',
            is_superuser = is_bussines,
            is_staff = is_bussines
        )
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Token {}'.format(
            self.token.key)
        

    def test_booking(self):

        #- The business can create a room with M capacity 
        self.setup_user("admin", "b@b.com", True)
        data = {
            "name": "test",
            "capacity": 1
        }
        room = self.client.post('/api/room/', data)
        self.assertEqual(booking_models.Room.objects.all().count(), 1)
        self.assertEqual(booking_models.Room.objects.all().first().user.is_superuser, True)
        self.assertEqual(booking_models.Room.objects.all().first().user.email, "b@b.com")
        
        #-- The client cant create a room with M capacity 
        self.setup_user("customer", "c@c.com", False)
        data = {
            "name": "test", #TODO: can test if unique
            "capacity": 1  #TODO: test different 
        }
        room = self.client.post('/api/room/', data)
        self.assertEqual(room.data, {'Message': 'Error'})

        #- The business can create events for every room. 
        self.setup_user("admin2", "b2@b2.com", True)
        data = {
            "name": "private_event", #TODO: can test if unique
            "room_id": 1,
            "is_private":True
        }
        event = self.client.post('/api/event/', data)
        self.assertEqual(booking_models.Event.objects.all().first().user.is_superuser, True)
        self.assertEqual(booking_models.Event.objects.all().count(), 1)
        data = {
            "name": "public_event", 
            "room_id": 1,
            "is_private":False
        }
        event = self.client.post('/api/event/', data)
        self.assertEqual(booking_models.Event.objects.all().first().user.is_superuser, True)
        self.assertEqual(booking_models.Event.objects.all().count(), 2)

        #- The client cant create events for every room. 
        self.setup_user("customer2", "c2@c.com", False)
        data = {
            "name": "event_fail", 
            "room_id": 1,
            "is_private":False
        }
        event = self.client.post('/api/event/', data)
        self.assertEqual(event.data, {"Message": "Error"})

        #- A customer can see all the available public events. 
        self.setup_user("customer3", "c3@c.com", False)
        events = self.client.get('/api/event/')
        self.assertEqual(len(events.data), 1)

        #- A Bussines can see all the available public and private events. 
        self.setup_user("admin3", "b3@b.com", True)
        event = self.client.get('/api/event/')
        self.assertEqual(len(event.data), 2)

        #- A customer can book a place for an event.
        self.setup_user("customer4", "c4@c.com", False)
        booking = self.client.get('/api/booking/')
        self.assertEqual(len(booking.data), 0)
        data = {
            "event_id": 1
        }
        booking = self.client.post('/api/booking/', data)
        self.assertEqual(booking.data, {"Message": "Okay"})
        self.assertEqual(booking_models.Booking.objects.all().count(), 1)

        #- A customer can cancel its booking for an event.
        booking_id = booking_models.Booking.objects.all().first().id
        booking = self.client.delete(f'/api/booking/{booking_id}/', data)
        self.assertEqual(booking.data, {"Message": "Okay"})
        self.assertEqual(booking_models.Booking.objects.all().count(), 0)

        #- The business can delete a room if said room does not have any events.
        self.setup_user("admin4", "b4@b.com", True)
        delete_room = self.client.delete(f'/api/room/1/')
        #- Cant delete room with events
        self.assertEqual(delete_room.data, {"Message": "Error"})
        room = self.client.post('/api/room/', data)
        delete_room = self.client.delete(f'/api/room/2/')
        #- Can delete room without events
        self.assertEqual(delete_room.data, {"Message": "Okay"})


