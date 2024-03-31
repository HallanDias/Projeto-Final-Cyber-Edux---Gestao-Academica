from django.contrib.auth.models import User
from django.db import models

class Aluno(models.Model):
    id = models.AutoField(primary_key=True)
    cpf = models.IntegerField()
    nome = models.TextField()
    data_nasc = models.DateField()
    sexo = models.TextField()
    nome_mae = models.TextField()
    naturalidade = models.TextField()
    data = models.DateField()
    image = models.ImageField(upload_to="imagens/")
    cep = models.CharField(max_length=8, blank=True, null=True)
    rua = models.TextField()
    bairro = models.TextField()
    numero = models.IntegerField(null=True, blank=True)
    complemento = models.TextField()
    cidade = models.TextField()
    uf = models.TextField()
    matricula = models.TextField()
    periodo = models.TextField()
    curso = models.TextField()

class Turma(models.Model):
    id = models.AutoField(primary_key=True)
    # Adicione os campos relevantes para a turma aqui

class NotaAluno(models.Model):
    id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    nota1 = models.DecimalField(max_digits=5, decimal_places=2)
    nota2 = models.DecimalField(max_digits=5, decimal_places=2)
    nota3 = models.DecimalField(max_digits=5, decimal_places=2)
    media = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.TextField(default='')

