from rest_framework.serializers import ModelSerializer
from api.models import Room,Event,Booking

class RoomSerializer(ModelSerializer):

    class Meta:
        model = Room
        depth = 2
        fields = '__all__'

class EventSerializer(ModelSerializer):

    class Meta:
        model = Event
        depth = 2
        fields = '__all__'

class BookingSerializer(ModelSerializer):

    class Meta:
        model = Booking
        depth = 2
        fields = '__all__'
