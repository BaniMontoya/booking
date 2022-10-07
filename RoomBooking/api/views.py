from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from api import serializers as api_serializers
from api import models as booking_models
from rest_framework.permissions import IsAuthenticated


class RoomViewSet(ViewSet):
    '''

    '''

    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = booking_models.Room.objects.order_by('pk')
        serializer = api_serializers.RoomSerializer(
            queryset, many=True)
        return Response(serializer.data, status=200)

    def create(self, request):
        data = request.data
        if not request.user.is_superuser:
            return Response({"Message": "Error"}, status=401)

        create = booking_models.Room.objects.create(user=request.user,
            name=data.get("name",""),capacity=data.get("capacity",1))
        return Response({"Message": "Okay"}, status=201)

    def retrieve(self, request, pk=None):
        queryset = booking_models.Room.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = api_serializers.RoomSerializer(item)
        return Response(serializer.data, status=200)

    def update(self, request, pk=None):
        try:
            item = booking_models.Room.objects.get(pk=pk)
        except booking_models.Room.DoesNotExist:
            return Response(status=404)
        serializer = api_serializers.RoomSerializer(
            item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = booking_models.Room.objects.get(pk=pk)
        except booking_models.Room.DoesNotExist:
            return Response({"Message": "Error 404"},status=404)
        try:
            item.delete()
            return Response({"Message": "Okay"}, status=200)
        except:
            return Response({"Message": "Error"}, status=401)


class EventViewSet(ViewSet):
    '''

    '''

    permission_classes = (IsAuthenticated,)

    def list(self, request):
        if request.user.is_staff:
            queryset = booking_models.Event.objects.order_by('pk')
            serializer = api_serializers.EventSerializer(
                queryset, many=True)
        else:
            queryset = booking_models.Event.objects.filter(is_private=False).order_by('pk')
            serializer = api_serializers.EventSerializer(
                queryset, many=True)
        return Response(serializer.data)


    def create(self, request):
        data = request.data
        if not request.user.is_superuser:
            return Response({"Message": "Error"}, status=401)

        create = booking_models.Event.objects.create(user=request.user,
            name=data.get("name",""),room_id=data.get("room_id",None), is_private=data.get("is_private",True))
        return Response({"Message": "Okay"}, status=201)

    def retrieve(self, request, pk=None):
        queryset = booking_models.Room.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = api_serializers.RoomSerializer(item)
        return Response(serializer.data, status=401)

    def update(self, request, pk=None):
        try:
            item = booking_models.Room.objects.get(pk=pk)
        except booking_models.Room.DoesNotExist:
            return Response(status=404)
        serializer = api_serializers.RoomSerializer(
            item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=401)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = booking_models.Room.objects.get(pk=pk)
        except booking_models.Room.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class BookingViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = booking_models.Booking.objects.order_by('pk')
        serializer = api_serializers.BookingSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        event_id = data.get("event_id",None)
        event_obj = booking_models.Event.objects.filter(id=event_id)

        if not request.user.is_superuser:
            if event_obj.exists():
                create = booking_models.Booking.objects.create(user=request.user,
                event_id=data.get("event_id",None))
            else:
                return Response({"Message": "Error"}, status=401)
        else:
            if event_obj.filter(is_private=False).exists():
                create = booking_models.Booking.objects.create(user=request.user,
                    event_id=data.get("event_id",None))
            else:
                return Response({"Message": "Error"}, status=401)
        return Response({"Message": "Okay"}, status=201)

    def retrieve(self, request, pk=None):
        queryset = booking_models.Booking.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = api_serializers.BookingSerializer(item)
        return Response(serializer.data, status=200)

    def update(self, request, pk=None):
        try:
            item = booking_models.Booking.objects.get(pk=pk)
        except booking_models.booking.DoesNotExist:
            return Response(status=404)
        serializer = api_serializers.BookingSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = booking_models.Booking.objects.get(pk=pk)
        except booking_models.booking.DoesNotExist:
            return Response({"Message": "Error"},status=404)
        item.delete()
        return Response({"Message": "Okay"},status=204)


