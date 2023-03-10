from django.shortcuts import render
from django.http import HttpResponse 
from .models import Book, Author, BookInstance, Genre 
from django.views import generic
# Create your views here.
 
# Create your views here. 
# def index(request): 
# 	return HttpResponse("Глaвнaя страница сайта Мир книг!") 

def index(request): 
	# Генерация "количеств" некотор�,IХ главньIХ объектов 
	num_books = Book.objects.all().count() 
	num_instances = BookInstance.objects.all().count() 
	# Доступные книги (статус= 'На складе') 
	num_instances_available = BookInstance.objects.filter().count() 
	# Авторы книг, 
	num_authors = Author.objects.count() # метод all() применен по умолчанию

	# количество посещений этого view, подсчитанное в переменной session
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1

	# Отрисовка НТМL-шаблона index.html с данными внутри переменной context 
	return render(request, 'index.html', 
				context={'num_books': num_books, 
				'num_instances': num_instances, 
				'num -instances_available': num_instances_available, 
				'num_authors': num_authors,
				'num_visits': num_visits}
			)

class BookListView(generic.ListView): 
	model = Book
	paginate_by = 3


class BookDetailView(generic.DetailView): 
	model = Book

class AuthorListView(generic.ListView): 
	model = Author 
	paginate_by = 4

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView): 
	'''
	Универсальный класс представления списка книг, 
	находящихся в заказе у текущего пользователя. 
	''' 
	model = BookInstance 
	template_name ='catalog/bookinstance_list_borrowed_user.html' 
	paginate_by = 10

	def get_queryset(self): 
		return BookInstance.objects.filter(borrower=self.request.user).filter(status='2').order_by('due_back') 
	

from django.http import * 
from django.shortcuts import render 
from .forms import AuthorsForm 
# получение данных из БД и загрузка шаблона authors add.html 
def authors_add(request): 
	author = Author.objects.all() 
	authorsform = AuthorsForm() 
	return render(request, "catalog/authors_add.html", {" form": authorsform, "author" : author}) 

def create(request): 
	if request.method == "POST": 
		author = Author() 
		author.first_name = request.POST.get("first_name") 
		author.last_name = request.POST.get("last_name") 
		author.date_of_birth = request.POST.get("date_of_birth") 
		author.date_of_death = request.POST.get("date_of_death") 
		author.save() 
		return HttpResponseRedirect("/authors_add/") 

# удаление авторов иэ БД 
def delete(request, id): 
	try: 
		author = Author.objects.get(id=id) 
		author.delete() 
		return HttpResponseRedirect("/authors_add/") 
	except Author.DoesNotExist: 
		return HttpResponseNotFound("<h2>Aвтop не найден</h2>") 

# изменение данных в БД 
def edit1(request, id): 
	author = Author.objects.get(id=id) 
	if request.method == "POST": 
		author.first_name = request.POST.get("first_name") 
		author.last_name = request.POST.get("last_name") 
		author.date_of_birth = request.POST.get("date_of_birth") 
		author.date_of_death = request.POST.get("date_of_death") 
		author.save () 
		return HttpResponseRedirect("/authors_add/") 
	else: 
		return render(request, "catalog/edit1.html", {"author": author}) 

from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.urls import reverse_lazy 
from .models import Book 

class BookCreate(CreateView): 
	model = Book 
	fields = '__all__' 
	success_url = reverse_lazy('books') 

class BookUpdate(UpdateView): 
	model = Book 
	fields = '__all__' 
	success_url = reverse_lazy('books') 

class BookDelete(DeleteView): 
	model = Book 
	success_url = reverse_lazy('books') 