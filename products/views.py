from django.views import generic
from django.shortcuts import get_object_or_404, reverse, render
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.contrib import messages


from .models import Product, Comment, Category
from .forms import CommentForm


class ProductListView(generic.ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug, is_active=True)
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['category'] = None
        if self.kwargs.get('category_slug'):
            context['category'] = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return context


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForm

    # def get_success_url(self):
    #     return reverse('product_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        product_id = int(self.kwargs['product_id'])
        product = get_object_or_404(Product, id=product_id)
        obj.product = product

        messages.success(self.request, _('Comment successfully created'))

        return super().form_valid(form)

