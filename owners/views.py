from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import PropertyOwner, InteractionLog
from .forms import PropertyOwnerForm, InteractionLogForm


def owner_list(request):
    query = request.GET.get('q', '')
    rating_filter = request.GET.get('rating', '')
    active_filter = request.GET.get('active', 'true')
    
    owners = PropertyOwner.objects.all()
    
    if query:
        owners = owners.filter(
            Q(name__icontains=query) | 
            Q(email__icontains=query) | 
            Q(company_name__icontains=query) |
            Q(phone__icontains=query)
        )
    
    if rating_filter:
        owners = owners.filter(overall_rating=rating_filter)
    
    if active_filter == 'true':
        owners = owners.filter(is_active=True)
    elif active_filter == 'false':
        owners = owners.filter(is_active=False)
    
    paginator = Paginator(owners, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'owners': page_obj.object_list,
        'query': query,
        'rating_filter': rating_filter,
        'active_filter': active_filter,
    }
    return render(request, 'owners/owner_list.html', context)


def owner_detail(request, pk):
    owner = get_object_or_404(PropertyOwner, pk=pk)
    interactions = owner.interactions.all()
    
    context = {
        'owner': owner,
        'interactions': interactions,
    }
    return render(request, 'owners/owner_detail.html', context)


def owner_create(request):
    if request.method == 'POST':
        form = PropertyOwnerForm(request.POST)
        if form.is_valid():
            owner = form.save()
            messages.success(request, f'Property owner {owner.name} created successfully!')
            return redirect('owner_detail', pk=owner.pk)
    else:
        form = PropertyOwnerForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'owners/owner_form.html', context)


def owner_update(request, pk):
    owner = get_object_or_404(PropertyOwner, pk=pk)
    if request.method == 'POST':
        form = PropertyOwnerForm(request.POST, instance=owner)
        if form.is_valid():
            owner = form.save()
            messages.success(request, f'Property owner {owner.name} updated successfully!')
            return redirect('owner_detail', pk=owner.pk)
    else:
        form = PropertyOwnerForm(instance=owner)
    
    context = {'form': form, 'owner': owner, 'action': 'Update'}
    return render(request, 'owners/owner_form.html', context)


def owner_delete(request, pk):
    owner = get_object_or_404(PropertyOwner, pk=pk)
    if request.method == 'POST':
        owner_name = owner.name
        owner.delete()
        messages.success(request, f'Property owner {owner_name} deleted successfully!')
        return redirect('owner_list')
    
    context = {'owner': owner}
    return render(request, 'owners/owner_confirm_delete.html', context)


def interaction_create(request, owner_pk):
    owner = get_object_or_404(PropertyOwner, pk=owner_pk)
    if request.method == 'POST':
        form = InteractionLogForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.owner = owner
            interaction.save()
            messages.success(request, 'Interaction logged successfully!')
            return redirect('owner_detail', pk=owner.pk)
    else:
        form = InteractionLogForm()
    
    context = {'form': form, 'owner': owner}
    return render(request, 'owners/interaction_form.html', context)


def dashboard(request):
    total_owners = PropertyOwner.objects.count()
    active_owners = PropertyOwner.objects.filter(is_active=True).count()
    excellent_rated = PropertyOwner.objects.filter(overall_rating=5).count()
    average_rating = PropertyOwner.objects.values('overall_rating').count()
    
    recent_interactions = InteractionLog.objects.all()[:5]
    
    context = {
        'total_owners': total_owners,
        'active_owners': active_owners,
        'excellent_rated': excellent_rated,
        'recent_interactions': recent_interactions,
    }
    return render(request, 'owners/dashboard.html', context)
