from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
def store(request, category_slug=None):
	catagories = None
	products = None

	if category_slug is not None:
		catagories = get_object_or_404(Category, slug=category_slug)
		products = Product.objects.filter(category=catagories, is_available=True)
		product_count = products.count()
		paginator = Paginator(products, 3)
		page = request.GET.get('page')
		page_products = paginator.get_page(page)

	else:
		products = Product.objects.all().filter(is_available=True)
		product_count = products.count()
		paginator = Paginator(products, 3)
		page = request.GET.get('page')
		page_products = paginator.get_page(page)

	context = {
		'products': page_products,
		'product_count': product_count,
	}

	return render(request, 'byteshop/store.html', context)


def product_detail(request, category_slug, product_slug):
	try:
		single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
		in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
	except Exception as e:
		raise e
	context = {
		'single_product': single_product,
		'in_cart': in_cart,
	}

	return render(request, 'byteshop/product_detail.html', context)
