from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util


class SearchForm(forms.Form):
    search_ = forms.CharField(label="Search Entries")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def entry_page(request, title):
    return render(request, "encyclopedia/entry_page.html", {
        "content": util.get_entry(title),
        "page_title": title,
        "form": SearchForm()
    })

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_ = form.cleaned_data["search_"]
            if util.get_entry(search_):
                return render(request, "encyclopedia/search.html", {
                    "form": form,
                    "search_": search_,
                    "titles": util.get_entry(search_),
                    "page_title": search_,
                })
            else:
                entry_list = []
                for i in util.list_entries():
                        if search_.capitalize() in i.capitalize():
                            entry_list.append(i)
                return render(request, "encyclopedia/search.html", {
                    "form": form,
                    "search_": search_,
                    "titles": util.get_entry(search_),
                    "page_title": search_,
                    "entries": util.list_entries(),
                    "entry_list": entry_list
                })
        else:
            return render(request, "encyclopedia/search.html", {
                "form": form
            })

def new_page(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "entries": util.list_entries(),
                "form": SearchForm()
            })
        if len(title)>1 and len(content)>1:
            util.save_entry(title, content)
            return render(request, "encyclopedia/new_page.html", {
                "entries": util.list_entries(),
                "form": SearchForm()
            })
        else:
            return render(request, "encyclopedia/new_page.html", {
                "entries": util.list_entries(),
                "form": SearchForm()
            })
    else:
        return render(request, "encyclopedia/new_page.html", {
            "entries": util.list_entries(),
            "form": SearchForm()
        })
    
def edit_page(request, title):
    if request.method == "POST":
        content = request.POST['content']
        if len(content)>1:
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry_page.html", {
                "content": util.get_entry(title),
                "page_title": title,
                "entries": util.list_entries(),
                "form": SearchForm()
            })
        else:
            return render(request, "encyclopedia/edit_page.html", {
                "entries": util.list_entries(),
                "form": SearchForm()
            })
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit_page.html", {
            "content": content,
            "title": title,
            "entries": util.list_entries(),
            "form": SearchForm()
        })