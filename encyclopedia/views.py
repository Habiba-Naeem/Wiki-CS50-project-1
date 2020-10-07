from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import markdown2
from markdown2 import Markdown
from . import util
from django.urls import reverse
import re, random
from random import choice    
from django.contrib import messages

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, string):
    entry = util.get_entry(string)
    if entry:
        markdowner = Markdown()
        filename = markdowner.convert(entry)
        print(filename)
        return render(request, "encyclopedia/page.html", {
                "filename": filename,
                "string":string
            })
    else:
        return render(request, "encyclopedia/error.html", {
            "filename": string
        })
    
def search(request):
    if request.method == "GET":
        q = request.GET["q"]
        entry = util.get_entry(q)
        print(entry)
        if entry:
            return redirect("entry_page", q)
        else:
            entries =  util.list_entries()
            substring = []
            for entry in entries:
                print(entry)
                print(entry.find(q))
                if re.search(q, entry, re.IGNORECASE):
                    substring.append(entry)
                    print(substring)

            if substring:
                return render(request, "encyclopedia/index.html", {
                "entries": substring
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "filename": q
                })

def new(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if util.get_entry(title):
            print("exists")
            messages.warning(request, "The entry already exists")
            return render(request, 'encyclopedia/new.html')
        else:
            print("save")
            details = request.POST.get("details")
            util.save_entry(title,details)
            return redirect("entry_page", title)

    return render(request, 'encyclopedia/new.html')

def edit(request, string):
    if request.method == "POST":
        details = request.POST.get("details")
        util.save_entry(string,details)
        return redirect("entry_page", string)
    else:
        entry = util.get_entry(string)
        context = {
            "string": string,
            "details": entry
        }
        return render(request, "encyclopedia/edit.html", context)

def randomm(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return redirect("entry_page", entry)