## Django dotnet communicator

# Functionalities
Provides a boilerplate project to communicate with a dotnet client.

# Environment variables
Located in the .env file.

# Running the project
1. pip install -r requirements.txt;
2. python manage.py runserver;
3. have the dotnet client running.

# Structure
1. Has a main_app project, which includes the main functionalities;
2. The `core` package contains a class `dll_runner`, which provides
the basic to run the dotnet client. The views use this class;
3. The `core` package also contains the `serializers.py` file, which
provides the serialization of the data to be sent to the dotnet client.
