import json

import clr
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.dll_runner import DllRunner
from core.serializers import BaseSerializer
from django_dotnet_communicator.main_app.models import BaseModel


def initialize_framework_dll():
    """
    A function to initialize the dll runner with the required dlls and imports
    :return: the initialized dll runner object
    """
    path = r'C:\Appl\Projects\C#\testrunner-interfaces\Festo.AST.Testrunner.Interfaces\Festo.AST.Testrunner.Interfaces.NFCL\bin\Debug'

    name = 'Festo.AST.Testrunner.Interfaces.NFCL'
    imports = [
        {
            'Festo.AST.Testrunner.Interfaces.NFCL.Entities': [
                'Device',
                'Project',
            ]
        },
        {
            'Festo.AST.Testrunner.Interfaces.NFCL.Utils': [
                'JsonMethodsCollection',
                'RestCommandsCollection',
            ]
        },
        {
            'Festo.AST.Testrunner.Interfaces.NFCL.G0_ConfigurationPlc': [
                'G00_RequestPlcMetaData',
                'G01_ResponsePlcMetaData',
            ]
        }
    ]
    runner = DllRunner()
    runner.register_dll(name, path)
    runner.handle_imports(*imports)
    return runner


def initialize_core_dll():
    """
    A function to initialize the dll runner with the required dlls and imports
    :return: the initialized dll runner object
    """
    path = r'C:\Appl\Projects\C#\testrunner-interfaces\Festo.AST.Testrunner.Interfaces\Festo.AST.Testrunner.Interfaces\bin\Debug\net6.0'

    name = 'Festo.AST.Testrunner.Interfaces'
    imports = [
        {
            'Festo.AST.Testrunner.Interfaces.Entities': [
                'Device',
                'Project',
            ]
        },
        {
            'Festo.AST.Testrunner.Interfaces.G0_ConfigurationPlc': [
                'G00_RequestPlcMetaData',
                'G01_ResponsePlcMetaData',
            ]
        }
    ]
    runner = DllRunner()
    runner.register_dll(name, path)
    runner.handle_imports(*imports)
    return runner


@api_view(['GET'])
def index_view(request):
    """
    A sample view that returns a list of all items
    @param request: the request object
    @return: a response with the list of all items
    """
    all_objects = BaseModel.objects.all()
    serializer = BaseSerializer(all_objects, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def post_view(request):
    """
    A sample view that receives a POST request
    @param request: the request object
    @return: a response with the received data
    """
    # ----------------------------------------------
    # default logic
    # ----------------------------------------------
    # serializer = BaseSerializer(data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data)
    #
    # return Response(serializer.errors, status=400)

    # ----------------------------------------------
    # dll logic
    # ----------------------------------------------
    request_data = request.data                                 # {'idOfPlcToRequest': '123'}
    """
    {'idOfPlcToRequest': '123'} is a valid JSON object, but it's represented as a Python dictionary. In Python, a 
    JSON object and a dictionary are similar data structures, but they are not the same. Therefore, you need to 
    convert the dictionary to a JSON-formatted string using json.dumps() before passing it to the method.
    """
    request_data_json_string = json.dumps(request_data)         # '{"idOfPlcToRequest": "123"}'

    dll_runner = initialize_framework_dll()
    # dll_runner = initialize_core_dll()

    g00_template_object = dll_runner.G00_RequestPlcMetaData()   # object of G00_RequestPlcMetaData class
    """
    ConvertFromJson is a static method, so it is called on the class
    """
    deserialized_g00 = g00_template_object.ConvertFromJson(request_data_json_string)    # object
    id_of_plc_to_request = deserialized_g00.IdOfPlcToRequest                            # string: 'W'

    new_device1 = dll_runner.Device("id1", "1", id_of_plc_to_request)               # object of Device class
    new_device2 = dll_runner.Device("id2", "2", id_of_plc_to_request)               # object of Device class
    new_device3 = dll_runner.Device("id1", "3", id_of_plc_to_request)               # object of Device class
    new_device_list = [new_device1, new_device2, new_device3]                       # list of objects of Device class
    dotnet_device_list = clr.System.Collections.Generic.List[dll_runner.Device]()   # list of objects of Device class
    [dotnet_device_list.Add(device) for device in new_device_list]
    new_project = dll_runner.Project("1", "2", "3", 9, dotnet_device_list)          # object of Project class

    g01_template_object = dll_runner.G01_ResponsePlcMetaData()               # object of G01_ResponsePlcMetaData class
    g01_template_object.Project = new_project                                # object of Project class
    response = g01_template_object.ConvertToJson()
    """
    response looks like this:
    
        {
          "project":{
              "projectname":"1",
              "projectpath":"2",
              "githash":"3",
              "topologytype":9,
              "devicesinthetopology":[
                  {"deviceid":"id1","ipaddress":"1","devicetype":"123"},
                  {"deviceid":"id2","ipaddress":"2","devicetype":"123"},
                  {"deviceid":"id1","ipaddress":"3","devicetype":"123"}
                  ]
             }
        }
    """
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_view(request, pk):
    """
    A sample view that receives a GET request
    @param request: the request object
    @param pk: the id of the object to retrieve
    @return: a response with the received data
    """
    try:
        item = BaseModel.objects.get(pk=pk)
    except (BaseModel.DoesNotExist, ValueError):
        return Response({'error': f'{BaseModel} not found'}, status=404)

    serializer = BaseSerializer(item)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
def edit_view(request, pk):
    """
    A sample view that receives a PUT or PATCH request
    @param request: the request object
    @param pk: the id of the object to update
    @return: a response with the updated data
    """
    try:
        item = BaseModel.objects.get(pk=pk)
    except (BaseModel.DoesNotExist, ValueError):
        return Response({'error': f'{BaseModel} not found'}, status=404)

    serializer = BaseSerializer(item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_view(request, pk):
    """
    A sample view that receives a DELETE request
    @param request: the request object
    @param pk: the id of the object to delete
    @return: a response with the deleted data
    """
    try:
        item = BaseModel.objects.get(pk=pk)
    except (BaseModel.DoesNotExist, ValueError):
        return Response({'error': f'{BaseModel} not found'}, status=404)

    item.delete()
    return Response({'message': f'{BaseModel} deleted successfully'})





