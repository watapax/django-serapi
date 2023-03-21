from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import (School, Account, License)

from api.task import Task

class LogInView(APIView):

    def post(self, request):

        try:

            # Get Form Data
            username = request.data['username']
            password = request.data['password']

            # Create Seed
            token = Task.create_seed()

            # Get Account
            account = Account.objects.get(username=username , password=password)

            # Get Licenses
            licenses_in_use = account.school.license_set.count()

            # Validate Licences in Use
            if licenses_in_use <= account.school.licenses - 1:

                # Add License Lisence
                license = License()
                license.school = account.school
                license.account = account
                license.token = token
                license.save()

                # Create License Response
                response = token

                # Create Error Response
                response = {
                    'school' : account.school.name,
                    'licenses' : {
                        'total' : account.school.licenses,
                        'available' : account.school.licenses - 1 - licenses_in_use,
                        'used' : licenses_in_use + 1
                    },
                    'token' : token,
                    'message' : 'Licenses recerved'
                }

            else:

                # Create Error Response
                response = {
                    'school' : account.school.name,
                    'licenses' : {
                        'total' : account.school.licenses,
                        'available' : account.school.licenses - licenses_in_use,
                        'used' : licenses_in_use
                    },
                    'message' : 'All licenses are in use'
                }

            return Response(response , status=status.HTTP_200_OK)
        
        except:
            
            # Create Error Response
            response = {
                'status' : 'Username does not exist'
            }

            return Response( response , status=status.HTTP_200_OK )

class LogOutView(APIView):

    def post(self , request):

        try:

            # Get Token
            token = request.data['token']

            # Get License
            license = License.objects.get(token=token)

            # Delete License
            license.delete()

            return Response( 'License Released' , status=status.HTTP_200_OK )

        except:

            return Response( 'Token does not exist' , status=status.HTTP_200_OK )

class LoggedView(APIView):

    def post(self, request):

        try:

            # Get Token
            token = request.data['token']

            # Get License
            license = License.objects.get(token=token)
            license.reserved = datetime.now()
            license.save()

            return Response( 'extended license' , status=status.HTTP_200_OK )

        except:

            return Response( 'Token does not exist' , status=status.HTTP_200_OK )
