from django.shortcuts import render
from django.utils import timezone
from .models import Post #The dot before models means current directory or current application. Both views.py and models.py are in the same directory. This means we can use . and the name of the file (without .py). Then we import the name of the model (Post).
from django.shortcuts import render, get_object_or_404


# Create your views here.

# we created a function (def) called post_list that takes request and will return the value it gets from calling another function render that will render (put together) our template blog/post_list.html.

# views are supposed to do: connect models and templates. In our post_list view we will need to take the models we want to display and pass them to the template. In a view we decide what (model) will be displayed in a template.

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date') # we want published blog posts sorted by         published_date
	# variable for our QuerySet: posts. Treat this as the name of our QuerySet. 
	return render(request, 'blog/post_list.html', {'posts': posts})
	# In the render function we have one parameter request (everything we receive from the user via the Internet) and another giving the template file ('blog/post_list.html'). The last parameter, {}, is a place in which we can add some things for the template to use. We need to give them names (we will stick to 'posts' right now). :) It should look like this: {'posts': posts}. 

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk) # we want to get one and only one blog post. To do this, we can use querysets, like this: Post.objects.get(pk=pk). get_object_or_404. In case there is no Post with the given pk, it will display much nicer page, the Page Not Found 404 page.
    return render(request, 'blog/post_detail.html', {'post': post})
