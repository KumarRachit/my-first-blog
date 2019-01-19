from django.shortcuts import render
from django.utils import timezone
from .models import Post #The dot before models means current directory or current application. Both views.py and models.py are in the same directory. This means we can use . and the name of the file (without .py). Then we import the name of the model (Post).
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect # "go to the post_detail page for the newly created post"


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

# When we submit the form, we are brought back to the same view, but this time we have some more data in request, more specifically in request.POST (the naming has nothing to do with a blog "post"; it's to do with the fact that we're "posting" data). Remember how in the HTML file, our <form> definition had the variable method="POST"? All the fields from the form are now in request.POST. You should not rename POST to anything else (the only other valid value for method is GET, but we have no time to explain what the difference is).So in our view we have two separate situations to handle: first, when we access the page for the first time and we want a blank form, and second, when we go back to the view with all form data we just typed. So we need to add a condition (we will use if for that):

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST) # If method is POST then we want to construct the PostForm with data from the form, right? We will do that as follows: form = PostForm(request.POST)
        if form.is_valid(): # The next thing is to check if the form is correct (all required fields are set and no incorrect values have been submitted). We do that with form.is_valid().
            post = form.save(commit=False) # Basically, we have two things here: we save the form with form.save and we add an author (since there was no author field in the PostForm and this field is required). commit=False means that we don't want to save the Post model yet – we want to add the author first. Most of the time you will use form.save() without commit=False, but in this case, we need to supply it. post.save() will preserve changes (adding the author) and a new blog post is created!
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk) # post_detail is the name of the view we want to go to. Remember that this view requires a pk variable? To pass it to the views, we use pk=post.pk, where post is the newly created blog post!
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})# To create a new Post form, we need to call PostForm() and pass it to the template.

def post_edit(request, pk): # we pass an extra pk parameter from urls.
    post = get_object_or_404(Post, pk=pk) # we get the Post model we want to edit with get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post) #  when we create a form, we pass this post as an instance, both when we save the form…
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
