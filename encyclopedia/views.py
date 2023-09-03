import random
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from . import util
import markdown2
from django.shortcuts import render,redirect, get_object_or_404

class NewTaskForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)


def index(request):
    entries = util.list_entries()
    rand = random.choice(entries)
    return render(request, "encyclopedia/index.html", {
        "random": rand,
        "entries": entries
    })
    
def add(request):
    entries = util.list_entries()
    rand = random.choice(entries)
    if request.method=='POST':
        form=NewTaskForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["content"]
            if util.get_entry(title):
                 return render(request,"encyclopedia/add.html",{
                 "form":form,
                   "random": rand,
                 "bool":True
                
        })
            else:
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("getPage",args=(title,)))
        else: return render(request,"encyclopedia/add.html",{
            "form":form,
            "random": rand,
        })
    return render(request,"encyclopedia/add.html",{
        "form":NewTaskForm(),
        "random": rand,
    })
def getPage(request,title):
    entries = util.list_entries()
    rand = random.choice(entries)
    page=util.get_entry(title)
    if page:
        return render(request,"encyclopedia/ContentPage.html",{
       "title":title,
       "content":markdown2.markdown(page),
        "bool":True,
        "random": rand,
        })
    else: return render(request,"encyclopedia/ContentPage.html",{
        "bool":False,
         "random": rand,
        })
    
def edit(request, title):
    initial_data = {
        'title' : title,
        'content' : util.get_entry(title)
    }
    entries = util.list_entries()
    rand = random.choice(entries)
    if request.method == 'POST':
        form =NewTaskForm(request.POST, initial=initial_data)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("getPage",args=(title,)))
    return render(request,"encyclopedia/edit.html",{
        "title":title,
        "form":NewTaskForm(initial=initial_data),
        "random": rand,
    })
def search_feature(request):
    entries = util.list_entries()
    rand = random.choice(entries)
    # Check if the request is a post request.
    if request.method == 'POST':
        # Retrieve the search query entered by the user
        search_query = request.POST['search_query']
        # Filter your model by the search query
        posts = filter(lambda entry: entry.casefold().__contains__(search_query.casefold() ), entries)
        posts=list(posts)
        if len(posts)>0:
            return render(request, "encyclopedia/search.html", {
            "random": rand,
            "entries": posts,
            "bool":True
            })
        else:
            return render(request, "encyclopedia/search.html", {
            "random": rand,
            "entries": posts,
            "bool":False
            })
   

   
