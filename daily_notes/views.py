from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from django.shortcuts import get_object_or_404

from daily_notes.models import (
    Day,
    Goal
)

from daily_notes.serializers import (
    DaySerializer,
    GoalSerializer,
)

class Index(APIView):
    def get(self, request:Request, *args, **kwargs):
        return Response([
            "Bienvenido al servidor bb <3",
            {
                "rutas":
                {
                    '<base>': [
                        {
                            'descripcion':'el indice, el lugar en el que estas ahorita',
                            'metodo':'GET',
                        },
                    ],
                    '<base>/goals/yyyy-mm/': [
                        {
                            'descripcion':'te dice todos las metas de un mes de un año',
                            'metodo':'GET',
                        },
                        {
                            'descripcion':'te permite crear metas especificando el titulo',
                            'metodo':'POST',
                        }
                    ],
                    '<base>/goals/id/<pk>/': [
                        {
                            'descripcion':'te permite cambiar el titulo o contenido de una meta',
                            'metodo':'PATCH',
                        },
                        {
                            'descripcion':'te permite borrar una meta',
                            'metodo':'DELETE',
                        }                                
                    ],
                    '<base>/days/yyyy-mm-dd/': [
                        {
                            'descripcion':'te permite ver todas las actividades de un dia',
                            'metodo':'GET',
                        },
                        {
                            'descripcion':'te permite modificar el texto de un dia',
                            'metodo':'POST',
                        },
                        {
                            'descripcion':'te permite eliminar todo el contenido de un dia',
                            'metodo':'DELETE',
                        }
                    ],
                    '<base>/search/?q=<busqueda>': [
                        {
                            'descripcion':'te permite buscar palabras o frases en los dias y meses',
                            'metodo':'GET',
                        }
                    ]
                }
            }
        ])

class SearchView(APIView):
    def get(self, request: Request, *args, **kwargs):
        param = request.query_params.get('q', None)

        if param is None:
            return Response("You must include a search parameter")

        goals = GoalSerializer(
            Goal.objects.filter(                #pylint: disable=no-member
                content__icontains=param
            ),
            many = True
        )

        days = DaySerializer(
            Day.objects.filter(                 #pylint: disable=no-member
                activities__icontains=param
            ),
            many = True
        )

        return Response(
            {
                'days':days.data,
                'goals':goals.data,
            }
        )

class GoalList(generics.ListCreateAPIView):
    serializer_class = GoalSerializer

    def parse_date(self):
        return self.kwargs['date']

    def get_queryset(self):
        year, month = self.parse_date()
        return Goal.objects.filter(year__exact = year, month__exact = month)    #pylint: disable=no-member

    def perform_create(self, serializer):
        year, month = self.parse_date()
        serializer.save(year=year, month=month)


class GoalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Goal.objects.all()                                               #pylint: disable=no-member
    serializer_class = GoalSerializer

class DayDetail(APIView):
    def get(self, request, date, *args, **kwargs):
        instance = get_object_or_404(Day, date=date)
        return DaySerializer(instance=instance).data

    def post(self, request, date, *args, **kwargs):
        instance, created = Day.objects.get_or_create(date=date)                #pylint: disable=no-member
        serializer = DaySerializer(instance=instance, data=request.data)
        serializer.save()
        
        response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=response_status)