from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    return render(request, "encyclopedia/entry_page.html", {
        "titles": util.get_entry(title),
        "page_title": title
    })