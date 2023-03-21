from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from .serializers import *
import json
from django.db.models import *

# Create your views here.
class TruckView (APIView):
    def get(self, request,pk=None):
        if pk:
            if Truck.objects.filter(pk=pk).exists():
                TruckData = Truck.objects.get(pk=pk)
                serializer = TruckSerializer(TruckData)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
        else:
            TruckData = Truck.objects.all()
            serializer = TruckSerializer(TruckData, many=True)
            return Response(serializer.data)

    def post(self, request):
        try:
            if Truck.objects.filter(Q(Plate_number=request.data['Plate_number']) | Q(Registration_number=request.data['Registration_number'])).exists():
                    return Response( 'Data Already Exist',status.HTTP_208_ALREADY_REPORTED)
            else:
                serializer = TruckSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)

    def put(self, request, pk):
        if Truck.objects.filter(pk=pk).exists():
            TruckData = Truck.objects.get(pk=pk)
            serializer = TruckSerializer(TruckData, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if Truck.objects.filter(pk=pk).exists():
            TruckData = Truck.objects.get(pk=pk)
            TruckData.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class DriverView (APIView):
    def get(self, request,pk=None,email=None,mobile_number=None,plate_number=None,language=None):
        if pk:
            if Driver.objects.filter(pk=pk).exists():
                DriverData = json.loads(json.dumps(DriverSerializer(Driver.objects.get(pk=pk)).data))
                TruckData = json.loads(json.dumps(TruckSerializer(Truck.objects.get(Truck_id=DriverData["Truck"])).data))
                DriverDetail = DriverData | TruckData
                del DriverDetail["Truck"]
                return Response(DriverDetail)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        if email:
            if Driver.objects.filter(Email=email).exists():
                DriverData = json.loads(json.dumps(DriverSerializer(Driver.objects.get(Email=email)).data))
                TruckData = json.loads(json.dumps(TruckSerializer(Truck.objects.get(Truck_id=DriverData["Truck"])).data))
                DriverDetail = DriverData | TruckData
                del DriverDetail["Truck"]
                return Response(DriverDetail)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        if mobile_number:
            print(mobile_number)
            if Driver.objects.filter(Mobile_number=mobile_number).exists():
                DriverData = json.loads(json.dumps(DriverSerializer(Driver.objects.get(Mobile_number=mobile_number)).data))
                TruckData = json.loads(json.dumps(TruckSerializer(Truck.objects.get(Truck_id=DriverData["Truck"])).data))
                DriverDetail = DriverData | TruckData
                del DriverDetail["Truck"]
                return Response(DriverDetail)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        if plate_number:
            print(plate_number)
            if Truck.objects.filter(Plate_number=plate_number).exists():
                TruckData = json.loads(json.dumps(TruckSerializer(Truck.objects.get(Plate_number=plate_number)).data))
                DriverData = json.loads(json.dumps(DriverSerializer(Driver.objects.get(Truck=TruckData["Truck_id"])).data))
                DriverDetail = DriverData | TruckData
                del DriverDetail["Truck"]
                return Response(DriverDetail)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        if language:
            print(language)
            DriverDetail = []
            if Driver.objects.filter(Language=language).exists():
                DriverData = json.loads(json.dumps(DriverSerializer(Driver.objects.filter(Language=language), many=True).data))
                for driver in DriverData:
                    print(driver)
                    TruckData = json.loads(json.dumps(TruckSerializer(Truck.objects.get(Truck_id=driver["Truck"])).data))
                    detail = driver| TruckData
                    del detail["Truck"]
                    DriverDetail.append(detail)
                return Response(DriverDetail)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            DriverDetail = []
            DriverData = Driver.objects.all()
            DriverData = json.loads(json.dumps(DriverSerializer(Driver.objects.all(), many=True).data))
            for driver in DriverData:
                print(driver)
                TruckData = json.loads(json.dumps(TruckSerializer(Truck.objects.get(Truck_id=driver["Truck"])).data))
                detail = driver| TruckData
                del detail["Truck"]
                DriverDetail.append(detail)
            return Response(DriverDetail)

    def post(self, request):
        try:
            if request.data['Truck_id']!="null":
                request.data['Email'] = request.data['Email'].lower()
                if Driver.objects.filter(Q(Email=request.data['Email']) | Q(Mobile_number=request.data['Mobile_number'])).exists():
                    return Response( 'Email or Mobile number Already Used',status.HTTP_208_ALREADY_REPORTED)
                else:
                    serializer = DriverSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                TruckData = TruckSerializer(data=request.data)
                if TruckData.is_valid():
                    TruckData.save()
                TruckDetail=json.loads(json.dumps(TruckSerializer(Truck.objects.get(Plate_number=request.data['Plate_number'])).data))
                request.data['Truck'] = TruckDetail['Truck_id']
                request.data['Email'] = request.data['Email'].lower()
                if Driver.objects.filter(Q(Email=request.data['Email']) | Q(Mobile_number=request.data['Mobile_number'])).exists():
                    return Response( 'Email or Mobile number Already Used',status.HTTP_208_ALREADY_REPORTED)
                else:
                    serializer = DriverSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except:
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)

    def put(self, request, pk):
        if Driver.objects.filter(pk=pk).exists():
            DriverData = Driver.objects.get(pk=pk)
            serializer = DriverSerializer(DriverData, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if Driver.objects.filter(pk=pk).exists():
            DriverData = Driver.objects.get(pk=pk)
            DriverData.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)