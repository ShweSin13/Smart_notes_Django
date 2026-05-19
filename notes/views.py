from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
import re


# 🧠 HOME / LIST VIEW + SEARCH
def note_list(request):
    query = request.GET.get('q')

    if query:
        notes = Note.objects.filter(title__icontains=query) | Note.objects.filter(content__icontains=query)
    else:
        notes = Note.objects.all()

    return render(request, 'notes/note_list.html', {
        'notes': notes,
        'query': query
    })


# 📄 NOTE DETAIL
def note_detail(request, pk):
    note = get_object_or_404(Note, id=pk)

    return render(request, 'notes/note_detail.html', {
        'note': note
    })


# 🟢 CREATE NOTE
def create_note(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        Note.objects.create(title=title, content=content)
        return redirect('note_list')

    return render(request, 'notes/create_note.html')


# 🟡 EDIT NOTE
def edit_note(request, pk):
    note = get_object_or_404(Note, id=pk)

    if request.method == "POST":
        note.title = request.POST.get("title")
        note.content = request.POST.get("content")
        note.save()

        return redirect('note_detail', pk=note.id)

    return render(request, 'notes/edit_note.html', {
        'note': note
    })


# 🔴 DELETE NOTE
def delete_note(request, pk):
    note = get_object_or_404(Note, id=pk)
    note.delete()

    return redirect('note_list')


# 🏷️ TAG FILTER SYSTEM (SMART + ROBUST)
def notes_by_tag(request, tag):
    tag = tag.lower()

    notes = []

    for note in Note.objects.all():

        # normalize content
        content = note.content.lower()

        # extract hashtags
        tags = re.findall(r"#(\w+)", content)

        # extract normal words
        words = re.findall(r"\b\w+\b", content)

        # match either hashtag OR plain word
        if tag in tags or tag in words:
            notes.append(note)

    return render(request, 'notes/note_list.html', {
        'notes': notes,
        'query': f"#{tag}"
    })