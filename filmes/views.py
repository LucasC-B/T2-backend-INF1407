from filmes.serializers import FilmeSerializer, FilmeAtualizaSerializer, FilmeCriaSerializer
from filmes.models import Filme
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.

@swagger_auto_schema(
            method = 'get',
            operation_summary="Dados de um filme",
            operation_description="Obter todas as informações sobre o filme selecionado",
            request_body=None,
            responses={200: FilmeSerializer(), 400: 'Mensagem de erro'},
            manual_parameters=[
                openapi.Parameter('titulo_filme', openapi.IN_PATH,
                                  default=5, type=openapi.TYPE_STRING,
                                  required=True, description='Titulo do filme na URL')
            ]
)
@api_view(['GET', ])
def api_detail_filme_view(request,slug):
    try:
        filme = Filme.objects.get(slug=slug)
    except Filme.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = FilmeSerializer(filme)
        return Response(serializer.data)


@swagger_auto_schema(
            method = 'put',
            operation_summary="Atualiza filme",
            operation_description="Atualizar um filme existente",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'titulo': openapi.Schema(default='', description='Titulo do filme', type=openapi.TYPE_STRING),
                    'nacionalidade': openapi.Schema(default='', description='Nacionalidade do filme', type=openapi.TYPE_STRING),
                    'ano': openapi.Schema(default='', description='Ano do filme', type=openapi.TYPE_INTEGER),
                    'sinopse': openapi.Schema(default='', description='Sinopse do filme', type=openapi.TYPE_STRING),
                    'diretor': openapi.Schema(default='', description='Diretor do filme', type=openapi.TYPE_STRING),
                    'nota': openapi.Schema(default='', description='Nota do filme', type=openapi.TYPE_INTEGER),
                    'review': openapi.Schema(default='', description='Review do filme', type=openapi.TYPE_STRING),
                    'visto': openapi.Schema(default='', description='Usuario viu o filme', type=openapi.TYPE_STRING),
                },
            ),
)
@api_view(['PUT', ])
@permission_classes([IsAuthenticated,])
def api_update_filme_view(request,slug):
    try:
        filme = Filme.objects.get(slug=slug)
    except Filme.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    if filme.usuario != user:
        return Response({'response':'Você não tem permissao para editar esse filme'})
    
    if request.method == "PUT":
        serializer = FilmeAtualizaSerializer(filme, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            print("aaa")
            data = {
                'response': 'Filme atualizado!',
                'pk' : filme.pk,
                'titulo' : filme.titulo,
                'nacionalidade' : filme.nacionalidade,
                'ano' : filme.ano,
                'sinopse' : filme.sinopse,
                'diretor' : filme.diretor,
                'nota' : filme.nota,
                'review' : filme.review,
                'visto' : filme.visto,
                'slug' : filme.slug,
            }
            
            return Response(data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
            method = 'delete',
            operation_description='Deleta filme',
            request_body=FilmeSerializer,
            responses={204: FilmeSerializer(), 400: None},
)
@api_view(['DELETE', ])
@permission_classes([IsAuthenticated,])
def api_delete_filme_view(request,slug):
    try:
        filme = Filme.objects.get(slug=slug)
    except Filme.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    if filme.usuario != user:
        return Response({'response':'Você não tem permissao para excluir esse filme!'})
    
    if request.method == "DELETE":
        operation = filme.delete()
        data = {}
        if operation:
            data["success"] = "Filme excluído com sucesso!"
        else:
            data["failure"] = "Filme não foi excluído!"
        
        return Response(data=data)

@swagger_auto_schema(
        method = 'post',
        operation_summary='Cria filme', 
        operation_description="Criar um novo filme",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'titulo': openapi.Schema(default='', description='Titulo do filme', type=openapi.TYPE_STRING),
                'nacionalidade': openapi.Schema(default='', description='Nacionalidade do filme', type=openapi.TYPE_STRING),
                'ano': openapi.Schema(default='', description='Ano do filme', type=openapi.TYPE_INTEGER),
                'sinopse': openapi.Schema(default='', description='Sinopse do filme', type=openapi.TYPE_STRING),
                'diretor': openapi.Schema(default='', description='Diretor do filme', type=openapi.TYPE_STRING),
                'nota': openapi.Schema(default='', description='Nota do filme', type=openapi.TYPE_INTEGER),
                'review': openapi.Schema(default='', description='Review do filme', type=openapi.TYPE_STRING),
                'visto': openapi.Schema(default='', description='Usuario viu o filme', type=openapi.TYPE_STRING),
            },
        ),
        responses={201: FilmeSerializer(), 400: 'Dados errados',},
)
@api_view(['POST', ])
@permission_classes([IsAuthenticated,])
def api_create_filme_view(request):
    if request.method == "POST":
        data = request.POST.copy()
        data.update(request.FILES)
        data['usuario'] = request.user.pk  # Adiciona o usuário diretamente
        serializer = FilmeCriaSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'response': 'Filme foi criado!'})
        else:
            return Response(serializer.errors, status=400)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApiFilmeListView(ListAPIView):
    queryset = Filme.objects.all()
    serializer_class = FilmeSerializer
    pagination_class = PageNumberPagination
        