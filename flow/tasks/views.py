from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProjectForm, TaskForm, CommentForm
from .models import Project, Task, Notification, TaskHistory, Comment


# ───────────────────────────────
# AUTENTICAÇÃO
# ───────────────────────────────

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'tasks/home.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = RegisterForm()
    return render(request, 'tasks/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bem-vindo de volta, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    else:
        form = AuthenticationForm()
        for field in form.fields.values():
            field.widget.attrs['class'] = 'form-control'
    return render(request, 'tasks/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da conta.')
    return redirect('login')


# ───────────────────────────────
# DASHBOARD
# ───────────────────────────────

@login_required(login_url='login')
def dashboard(request):
    my_projects = Project.objects.filter(owner=request.user)
    member_projects = request.user.projects.exclude(owner=request.user)
    notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]
    return render(request, 'tasks/dashboard.html', {
        'my_projects': my_projects,
        'member_projects': member_projects,
        'notifications': notifications,
    })


# ───────────────────────────────
# PROJETOS
# ───────────────────────────────

@login_required(login_url='login')
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.members.add(request.user)
            messages.success(request, f'Projeto "{project.name}" criado!')
            return redirect('project_detail', pk=project.pk)
        else:
            messages.error(request, 'Corrija os erros.')
    else:
        form = ProjectForm()
    return render(request, 'tasks/project_form.html', {'form': form, 'action': 'Criar'})


@login_required(login_url='login')
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user not in project.members.all():
        messages.error(request, 'Você não tem acesso a esse projeto.')
        return redirect('dashboard')
    tasks_todo  = project.tasks.filter(status='todo')
    tasks_doing = project.tasks.filter(status='doing')
    tasks_done  = project.tasks.filter(status='done')
    return render(request, 'tasks/project_detail.html', {
        'project': project,
        'tasks_todo': tasks_todo,
        'tasks_doing': tasks_doing,
        'tasks_done': tasks_done,
    })


@login_required(login_url='login')
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user != project.owner:
        messages.error(request, 'Só o dono pode editar o projeto.')
        return redirect('project_detail', pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Projeto atualizado!')
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'tasks/project_form.html', {'form': form, 'action': 'Editar'})


@login_required(login_url='login')
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user != project.owner:
        messages.error(request, 'Só o dono pode excluir o projeto.')
        return redirect('project_detail', pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Projeto excluído.')
        return redirect('dashboard')
    return render(request, 'tasks/project_confirm_delete.html', {'project': project})


# ───────────────────────────────
# TAREFAS
# ───────────────────────────────

@login_required(login_url='login')
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)

    if request.user not in project.members.all():
        messages.error(request, 'Você não tem acesso a esse projeto.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = TaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            task.save()

            
            TaskHistory.objects.create(
                task=task,
                changed_by=request.user,
                change_description=f'Tarefa criada com status "{task.get_status_display()}".'
            )

            
            if task.assigned_to and task.assigned_to != request.user:
                Notification.objects.create(
                    user=task.assigned_to,
                    message=f'{request.user.username} te atribuiu a tarefa "{task.title}" no projeto "{project.name}".'
                )

            messages.success(request, f'Tarefa "{task.title}" criada!')
            return redirect('project_detail', pk=project.pk)
        else:
            messages.error(request, 'Corrija os erros.')
    else:
        form = TaskForm(project=project)

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'project': project,
        'action': 'Criar'
    })


@login_required(login_url='login')
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project

    if request.user not in project.members.all():
        messages.error(request, 'Você não tem acesso a essa tarefa.')
        return redirect('dashboard')

    comments = task.comments.all().order_by('created_at')
    history  = task.history.all().order_by('-changed_at')
    form     = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task   = task
            comment.author = request.user
            comment.save()

    
            TaskHistory.objects.create(
                task=task,
                changed_by=request.user,
                change_description=f'{request.user.username} adicionou um comentário.'
            )

            
            if task.assigned_to and task.assigned_to != request.user:
                Notification.objects.create(
                    user=task.assigned_to,
                    message=f'{request.user.username} comentou na tarefa "{task.title}".'
                )

            
            if task.created_by != request.user and task.created_by != task.assigned_to:
                Notification.objects.create(
                    user=task.created_by,
                    message=f'{request.user.username} comentou na tarefa "{task.title}".'
                )

            messages.success(request, 'Comentário adicionado!')
            return redirect('task_detail', pk=task.pk)
        else:
            messages.error(request, 'Comentário não pode estar vazio.')

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'project': project,
        'comments': comments,
        'history': history,
        'comment_form': form,
    })


@login_required(login_url='login')
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project

    if request.user not in project.members.all():
        messages.error(request, 'Acesso negado.')
        return redirect('dashboard')

    old_status = task.status  

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, project=project)
        if form.is_valid():
            updated_task = form.save()

            
            if updated_task.status != old_status:
                old_label = dict(Task.STATUS_CHOICES)[old_status]
                new_label = updated_task.get_status_display()
                desc = f'Status alterado de "{old_label}" para "{new_label}".'

                TaskHistory.objects.create(
                    task=updated_task,
                    changed_by=request.user,
                    change_description=desc
                )

                
                if updated_task.assigned_to and updated_task.assigned_to != request.user:
                    Notification.objects.create(
                        user=updated_task.assigned_to,
                        message=f'A tarefa "{updated_task.title}" teve seu status alterado para "{new_label}".'
                    )

            messages.success(request, 'Tarefa atualizada!')
            return redirect('task_detail', pk=task.pk)
        else:
            messages.error(request, 'Corrija os erros.')
    else:
        form = TaskForm(instance=task, project=project)

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'project': project,
        'action': 'Editar'
    })


@login_required(login_url='login')
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project

    if request.user not in project.members.all():
        messages.error(request, 'Acesso negado.')
        return redirect('dashboard')

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Tarefa excluída.')
        return redirect('project_detail', pk=project.pk)

    return render(request, 'tasks/task_confirm_delete.html', {
        'task': task,
        'project': project
    })


@login_required(login_url='login')
def task_change_status(request, pk, new_status):
    """Muda o status direto do board sem abrir formulário."""
    task = get_object_or_404(Task, pk=pk)
    project = task.project

    if request.user not in project.members.all():
        messages.error(request, 'Acesso negado.')
        return redirect('dashboard')

    valid_statuses = ['todo', 'doing', 'done']
    if new_status not in valid_statuses:
        messages.error(request, 'Status inválido.')
        return redirect('project_detail', pk=project.pk)

    old_label = task.get_status_display()
    task.status = new_status
    task.save()
    new_label = task.get_status_display()

    TaskHistory.objects.create(
        task=task,
        changed_by=request.user,
        change_description=f'Status alterado de "{old_label}" para "{new_label}" pelo board.'
    )

    if task.assigned_to and task.assigned_to != request.user:
        Notification.objects.create(
            user=task.assigned_to,
            message=f'A tarefa "{task.title}" foi movida para "{new_label}".'
        )

    messages.success(request, f'Tarefa movida para "{new_label}".')
    return redirect('project_detail', pk=project.pk)




@login_required(login_url='login')
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    task    = comment.task

    # controla que só o autor do comentário pode editar
    if request.user != comment.author:
        messages.error(request, 'Só o autor pode excluir o comentário.')
        return redirect('task_detail', pk=task.pk)

    if request.method == 'POST':
        comment.delete()
        TaskHistory.objects.create(
            task=task,
            changed_by=request.user,
            change_description=f'{request.user.username} removeu um comentário.'
        )
        messages.success(request, 'Comentário excluído.')

    return redirect('task_detail', pk=task.pk)

# ───────────────────────────────
# MEMBROS DO PROJETO
# ───────────────────────────────

@login_required(login_url='login')
def project_add_member(request, pk):
    project = get_object_or_404(Project, pk=pk)

    
    if request.user != project.owner:
        messages.error(request, 'Só o dono pode adicionar membros.')
        return redirect('project_detail', pk=pk)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        try:
            from django.contrib.auth.models import User
            new_member = User.objects.get(username=username)

            if new_member in project.members.all():
                messages.warning(request, f'{username} já é membro deste projeto.')
            else:
                project.members.add(new_member)

                # Notifica o novo membro
                Notification.objects.create(
                    user=new_member,
                    message=f'{request.user.username} te adicionou ao projeto "{project.name}".'
                )
                messages.success(request, f'{username} adicionado ao projeto!')

        except User.DoesNotExist:
            messages.error(request, f'Usuário "{username}" não encontrado.')

    return redirect('project_detail', pk=pk)


@login_required(login_url='login')
def project_remove_member(request, pk, user_pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user != project.owner:
        messages.error(request, 'Só o dono pode remover membros.')
        return redirect('project_detail', pk=pk)

    if request.method == 'POST':
        from django.contrib.auth.models import User
        member = get_object_or_404(User, pk=user_pk)

        # Não pode remover o próprio dono
        if member == project.owner:
            messages.error(request, 'O dono não pode ser removido do projeto.')
        else:
            project.members.remove(member)
            Notification.objects.create(
                user=member,
                message=f'Você foi removido do projeto "{project.name}".'
            )
            messages.success(request, f'{member.username} removido do projeto.')

    return redirect('project_detail', pk=pk)


# ───────────────────────────────
# NOTIFICAÇÕES
# ───────────────────────────────

@login_required(login_url='login')
def notifications_view(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    # Marca todas como lidas ao abrir a página
    notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'tasks/notifications.html', {
        'notifications': notifications
    })


@login_required(login_url='login')
def notification_clear(request):
    """Apaga todas as notificações do usuário."""
    if request.method == 'POST':
        Notification.objects.filter(user=request.user).delete()
        messages.success(request, 'Notificações limpas.')
    return redirect('notifications')



# view de perfil 

@login_required(login_url='login')
def profile(request):
    my_projects  = Project.objects.filter(owner=request.user)
    my_tasks     = Task.objects.filter(assigned_to=request.user)
    tasks_done   = my_tasks.filter(status='done').count()
    tasks_doing  = my_tasks.filter(status='doing').count()
    tasks_todo   = my_tasks.filter(status='todo').count()

    return render(request, 'tasks/profile.html', {
        'my_projects':  my_projects,
        'my_tasks':     my_tasks,
        'tasks_done':   tasks_done,
        'tasks_doing':  tasks_doing,
        'tasks_todo':   tasks_todo,
    })