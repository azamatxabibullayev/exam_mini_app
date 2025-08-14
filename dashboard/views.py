from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from main.models import Topic, Test
from users.models import CustomUser
from django.contrib import messages
from django.core.paginator import Paginator


def is_custom_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


@login_required
@user_passes_test(is_custom_admin)
def dashboard_home(request):
    stats = {
        'total_users': CustomUser.objects.count(),
        'total_topics': Topic.objects.count(),
        'total_tests': Test.objects.count(),
    }

    import datetime
    from django.db.models.functions import TruncDate
    from django.db.models import Count

    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=6)
    users_per_day = CustomUser.objects.filter(date_joined__date__gte=last_week) \
        .annotate(day=TruncDate('date_joined')) \
        .values('day') \
        .annotate(count=Count('id')).order_by('day')

    chart_labels = [(last_week + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    chart_data = []
    for label in chart_labels:
        found = next((item['count'] for item in users_per_day if item['day'].strftime('%Y-%m-%d') == label), 0)
        chart_data.append(found)

    return render(request, 'dashboard/home.html',
                  {'stats': stats, 'chart_labels': chart_labels, 'chart_data': chart_data})


@login_required
@user_passes_test(is_custom_admin)
def user_list(request):
    users = CustomUser.objects.all().order_by('full_name')
    return render(request, 'dashboard/user_list.html', {'users': users})


@login_required
@user_passes_test(is_custom_admin)
def user_edit(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.full_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        user.is_active = 'is_active' in request.POST
        if request.user.is_superuser:
            user.is_staff = 'is_staff' in request.POST
        user.save()
        messages.success(request, "User updated successfully")
        return redirect('dashboard:user_list')
    return render(request, 'dashboard/user_edit.html', {'user': user})


@login_required
@user_passes_test(is_custom_admin)
def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully")
        return redirect('dashboard:user_list')
    return render(request, 'dashboard/user_delete.html', {'user': user})


@login_required
@user_passes_test(is_custom_admin)
def topic_list(request):
    search = request.GET.get('search', '')
    topics = Topic.objects.filter(name__icontains=search)
    paginator = Paginator(topics, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/topic_list.html', {'page_obj': page_obj, 'search': search})


@login_required
@user_passes_test(is_custom_admin)
def topic_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Topic.objects.create(name=name)
        messages.success(request, "Topic created successfully")
        return redirect('dashboard:topic_list')
    return render(request, 'dashboard/topic_form.html')


@login_required
@user_passes_test(is_custom_admin)
def topic_edit(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        topic.name = request.POST.get('name')
        topic.save()
        messages.success(request, "Topic updated successfully")
        return redirect('dashboard:topic_list')
    return render(request, 'dashboard/topic_form.html', {'topic': topic})


@login_required
@user_passes_test(is_custom_admin)
def topic_delete(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        topic.delete()
        messages.success(request, "Topic deleted successfully")
        return redirect('dashboard:topic_list')
    return render(request, 'dashboard/topic_delete.html', {'topic': topic})


@login_required
@user_passes_test(is_custom_admin)
def test_list(request):
    search = request.GET.get('search', '')
    tests = Test.objects.filter(title__icontains=search)
    paginator = Paginator(tests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/test_list.html', {'page_obj': page_obj, 'search': search})


@login_required
@user_passes_test(is_custom_admin)
def test_create(request):
    topics = Topic.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        topic_id = request.POST.get('topic')
        topic = get_object_or_404(Topic, pk=topic_id)
        Test.objects.create(title=title, topic=topic)
        messages.success(request, "Test created successfully")
        return redirect('dashboard:test_list')
    return render(request, 'dashboard/test_form.html', {'topics': topics})


@login_required
@user_passes_test(is_custom_admin)
def test_edit(request, pk):
    test = get_object_or_404(Test, pk=pk)
    topics = Topic.objects.all()
    if request.method == 'POST':
        test.title = request.POST.get('title')
        topic_id = request.POST.get('topic')
        test.topic = get_object_or_404(Topic, pk=topic_id)
        test.save()
        messages.success(request, "Test updated successfully")
        return redirect('dashboard:test_list')
    return render(request, 'dashboard/test_form.html', {'test': test, 'topics': topics})


@login_required
@user_passes_test(is_custom_admin)
def test_delete(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if request.method == 'POST':
        test.delete()
        messages.success(request, "Test deleted successfully")
        return redirect('dashboard:test_list')
    return render(request, 'dashboard/test_delete.html', {'test': test})
