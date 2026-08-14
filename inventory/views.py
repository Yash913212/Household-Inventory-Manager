from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.db.models import Count, Q, Sum
from .models import Location, Item
from .forms import LocationForm, ItemForm


# ==========================================
# Location Views
# ==========================================

class LocationListView(ListView):
    model = Location
    template_name = 'inventory/location_list.html'
    context_object_name = 'locations'

    def get_queryset(self):
        queryset = Location.objects.annotate(item_count=Count('items'))
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '').strip()
        context['total_locations'] = Location.objects.count()
        context['total_items'] = Item.objects.count()
        return context


class LocationCreateView(CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'inventory/location_form.html'
    success_url = reverse_lazy('location_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Add'
        return context


class LocationUpdateView(UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'inventory/location_form.html'
    success_url = reverse_lazy('location_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Edit'
        return context


class LocationDeleteView(DeleteView):
    model = Location
    template_name = 'inventory/location_confirm_delete.html'
    success_url = reverse_lazy('location_list')
    context_object_name = 'location'


# ==========================================
# Item Views
# ==========================================

class ItemListView(ListView):
    model = Item
    template_name = 'inventory/item_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = Item.objects.select_related('location').all()
        location_id = self.request.GET.get('location')
        search_query = self.request.GET.get('q', '').strip()

        if location_id:
            queryset = queryset.filter(location_id=location_id)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location__name__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locations'] = Location.objects.all()
        context['selected_location'] = self.request.GET.get('location', '')
        context['search_query'] = self.request.GET.get('q', '').strip()
        context['total_items_count'] = Item.objects.count()
        total_qty = Item.objects.aggregate(total=Sum('quantity'))['total']
        context['total_quantity_sum'] = total_qty if total_qty is not None else 0
        return context


class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('item_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Add'
        context['has_locations'] = Location.objects.exists()
        return context


class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('item_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Edit'
        context['has_locations'] = Location.objects.exists()
        return context


class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'inventory/item_confirm_delete.html'
    success_url = reverse_lazy('item_list')
    context_object_name = 'item'
