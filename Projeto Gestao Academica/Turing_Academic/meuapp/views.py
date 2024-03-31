from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from .models import Aluno, NotaAluno, Turma
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
from django.http import JsonResponse



def home(request):
    context = {
        'posts': Aluno.objects.all()
    }
    return render(request, 'home.html', context)



import re
@login_required(login_url='/login')
def cadastro_aluno(request):
    if request.method == 'POST':
        # Obtenha o CPF diretamente do request.POST
        cpf = request.POST.get('cpf', '')
        # Limpe o CPF removendo caracteres não numéricos
        cpf = re.sub('[^0-9]', '', cpf)
        if not validar_cpf(cpf):
            return render(request, 'publicate.html', {'error_message': 'CPF inválido'})

        nome = request.POST.get("nome")
        data_nasc = request.POST.get("data_nasc")
        try:
            data_nasc = datetime.strptime(data_nasc, '%Y-%m-%d').date()
        except ValueError:
            # Tratar erro de conversão, caso a data não esteja no formato esperado
            error_message = "Erro: Formato de data inválido"
            return render(request, 'publicate.html', {'error_message': error_message})
        sexo = request.POST.get("sexo")
        nome_mae = request.POST.get("nome_mae")
        naturalidade = request.POST.get("naturalidade")
        email = request.POST.get("email")
        cep = request.POST.get("cep")
        rua = request.POST.get("rua")
        numero = request.POST.get("numero")
        complemento = request.POST.get("complemento")
        cidade = request.POST.get("cidade")
        uf = request.POST.get("uf")
        matricula = request.POST.get("matricula")
        periodo = request.POST.get("periodo")
        curso = request.POST.get("curso")
        aluno = Aluno()
        aluno.user = request.user
        aluno.cpf = cpf
        aluno.nome = nome
        aluno.data_nasc = data_nasc
        aluno.sexo = sexo
        aluno.nome_mae = nome_mae
        aluno.naturalidade = naturalidade
        aluno.email = email
        aluno.cep = cep
        aluno.rua = rua
        aluno.numero = numero
        aluno.complemento = complemento
        aluno.cidade = cidade
        aluno.uf = uf
        aluno.image = request.FILES['image']
        aluno.data = date.today()
        aluno.matricula = matricula
        aluno.periodo = periodo
        aluno.curso = curso
        aluno.save()
        return HttpResponseRedirect('/')
    else:
        return render(request, 'publicate.html', {})
    

def validar_cpf(cpf):
    # Verifica se o CPF possui 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False

    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = 11 - (soma % 11)
    if resto == 10 or resto == 11:
        resto = 0
    if resto != int(cpf[9]):
        return False

    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = 11 - (soma % 11)
    if resto == 10 or resto == 11:
        resto = 0
    if resto != int(cpf[10]):
        return False

    return True



def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'incorrect_login': False 
        })
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'login.html', {
                'incorrect_login': True 
            })
    else:
        return HttpResponseBadRequest()



@login_required(login_url='/login')
def userspace_view(request):
    return render(request, 'userspace.html', {
        'username': request.user.username
    })



@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')



def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha1 = request.POST.get('senha1')
        # verifica se o nome do usuario ja existe
    if User.objects.filter(username=nome).exists():
        return HttpResponse(('Esse usuario ja existe'), redirect('/cadastro'))
    else:
        if senha == senha1:
            user = User.objects.create_user(nome, email, senha)
            user.save()
            login(request, user)
            return redirect('/login')
        else:
            return HttpResponse('Senhas não sao iguais') # Erro na autenticação da senha


def formulario_update(request, id):    
    pessoa = Aluno.objects.get(id=id)
    if request.method == 'POST':
        # Atualize os campos do objeto pessoa com os dados do formulário
        pessoa.cpf = request.POST.get('cpf')
        pessoa.nome = request.POST.get('nome')
        data_nasc = request.POST.get("data_nasc")
        try:
            data_nasc = datetime.strptime(data_nasc, '%Y-%m-%d').date()
        except ValueError:
            # Tratar erro de conversão, caso a data não esteja no formato esperado
            error_message = "Erro: Formato de data inválido"
            return render(request, 'publicate.html', {'error_message': error_message})
        pessoa.sexo = request.POST.get('sexo')
        pessoa.nome_mae = request.POST.get('nome_mae')
        pessoa.naturalidade = request.POST.get('naturalidade')
        pessoa.email = request.POST.get('email')
        pessoa.cep = request.POST.get('cep')
        pessoa.rua = request.POST.get('rua')
        pessoa.numero = request.POST.get('numero')
        pessoa.complemento = request.POST.get('complemento')
        pessoa.cidade = request.POST.get('cidade')
        pessoa.uf = request.POST.get('uf')
        pessoa.matricula = request.POST.get('matricula')
        pessoa.periodo = request.POST.get('periodo')
        pessoa.curso = request.POST.get('curso')
        # Se houver um novo arquivo de imagem, atualize-a
        if 'image' in request.FILES:
            pessoa.image = request.FILES['image']
        # Salve as alterações no objeto
        pessoa.save()
        # Redirecione o usuário para uma página de confirmação ou para a página inicial
        return redirect('/')

    return render(request, 'formulario_update.html', {'pessoa': pessoa})



def excluir_publicate(request, id):
    # Buscar a instância do modelo pelo ID ou retornar 404 se não existir
    publication = get_object_or_404(Aluno, id=id)
    
    # Verificar se a requisição é do tipo POST
    if request.method == 'POST':
        # Excluir a instância do modelo
        publication.delete()
        # Redirecionar para a página inicial ou outra página após a exclusão
        return redirect('/')  # Redirecionar para a página inicial ou outra página
    
    # Renderizar o template de confirmação de exclusão
    return render(request, 'excluir_publicate.html', {'post': publication})


'''
def capturar_foto(request):
    if request.method == 'POST' and request.FILES['foto']:
        nova_publicacao = Publication(image=request.FILES['foto'])
        nova_publicacao.save()
        return redirect('alguma_url')  # Redirecionar para onde desejar após salvar a foto
    return render(request, 'sua_template.html')

'''


def listagem_alunos(request):
    alunos = Aluno.objects.all()

    # Ordenar os alunos por nome
    alunos_ordenados = sorted(alunos, key=lambda x: x.nome)

    context = {'alunos': alunos_ordenados}
    return render(request, 'listagem_alunos.html', context)


def buscador(request):
    return render(request, 'buscador.html')


def search_students(request):
    search_value = request.GET.get('searchValue', '')
    # Verificar se o valor de entrada é um número (CPF)
    if search_value.isdigit():
        students = Aluno.objects.filter(cpf=search_value)
    else:
        students = Aluno.objects.filter(nome__icontains=search_value)
    data = [{'nome': student.nome, 'cpf': student.cpf, 'curso': student.curso, 'matricula': student.matricula, 'periodo': student.periodo} for student in students]
    return JsonResponse(data, safe=False)


def carregar_turmas(request):
    curso = request.GET.get('curso')
    periodo = request.GET.get('periodo')
    turmas = Aluno.objects.filter(curso=curso, periodo=periodo).values('id', 'nome')
    return JsonResponse(list(turmas), safe=False)


def lancar_nota(request):
    if request.method == 'POST':
        turma_id = request.POST.get('turma_id')
        notas = []

        # Aqui você processa as notas e as salva no banco de dados como já está fazendo
        # Depois, recupere as notas salvas para exibição

        notas = NotaAluno.objects.filter(turma_id=turma_id)

        return render(request, 'lancar_nota.html', {'notas': notas})

    return render(request, 'lancar_nota.html', {})
