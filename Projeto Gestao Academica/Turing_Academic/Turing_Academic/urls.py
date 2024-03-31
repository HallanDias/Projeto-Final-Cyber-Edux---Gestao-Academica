from django.urls import path
from meuapp import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('publicate/', views.cadastro_aluno, name='publicate'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('formulario_update/<int:id>', views.formulario_update, name="formulario_update"),
    path('excluir_publicate/<int:id>', views.excluir_publicate, name='excluir_publicate'),
    path('listagem_alunos/', views.listagem_alunos, name='listagem_alunos'),
    path('buscador/', views.buscador, name='buscador.html'),
    path('search_students/', views.search_students, name='search_students.html'),
    path('carregar_turmas/', views.carregar_turmas, name='carregar_turmas'),
    path('lancar_nota/', views.lancar_nota, name='lancar_nota'),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)