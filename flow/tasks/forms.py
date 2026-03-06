from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Task, Comment # adicionando os formulários de projeto e tarefa 
from django.contrib.auth.models import User #user built in do django relacionado a tarefas 


# Formulário de cadastro 
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='E-mail')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


# Formulário de projeto
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ex: Trabalho de Faculdade'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Descreva o projeto (opcional)',
            'rows': 3
        })
        
#form de tarefa 
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'assigned_to']

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)

        
        if project:
            self.fields['assigned_to'].queryset = project.members.all()
        else:
            self.fields['assigned_to'].queryset = User.objects.none()

        
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ex: Criar tela de login'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Descreva a tarefa (opcional)',
            'rows': 3
        })
        self.fields['status'].widget.attrs.update({'class': 'form-select'})
        self.fields['assigned_to'].widget.attrs.update({'class': 'form-select'})
        self.fields['assigned_to'].required = False
        self.fields['assigned_to'].label = 'Atribuir para'
        self.fields['assigned_to'].empty_label = 'Ninguém (sem atribuição)'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Escreva um comentário...',
            'rows': 3,
        })
        self.fields['text'].label = ''  