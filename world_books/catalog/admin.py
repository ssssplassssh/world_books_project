from django.contrib import admin

from catalog.models import Author, AuthorAdmin, Book, BookInstance, Genre, Language, Status

# Register your models here.

# admin.site.register(Author) 
# admin.site.register(Book) 
admin.site.register(Genre) 
admin.site.register(Language) 
admin.site.register(Status) 
# admin.site.register(BookInstance) 
admin.site.register(Author, AuthorAdmin) 

@admin.register(BookInstance) 
class BookInstanceAdmin(admin.ModelAdmin): 
	list_display = ('book', 'status', 'borrower', 'due_back', 'id')
	list_filter = ('status', 'due_back') 
	# fields = ['first_name', 'last_name', 
	#		('date_of_birth', 'date_of_death')] 
	fieldsets = (
		(None, {
			'fields' : ('book' , 'imprint' , 'inv_nom' )
			}), 
		('Availability', {
			'fields': ('status', 'due_back', 'borrower')
			}),
			)

class BooksInstanceInline(admin.TabularInline): 
	model = BookInstance 

@admin.register(Book) 
class BookAdmin(admin.ModelAdmin): 
	list_display = ('title', 'genre', 'language', 'display_author')
	list_filter = ('genre', 'author')  
	inlines = [BooksInstanceInline]	


