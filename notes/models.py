from django.db import models
from django.utils.safestring import mark_safe
import re


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # 🔗 Related notes
    def get_related_notes(self):
        words = self.content.lower().split()
        return Note.objects.filter(title__in=words).exclude(id=self.id)

    # 🔥 A1 Auto-linking
    def get_linked_content(self):
        content = self.content
        notes = Note.objects.all()

        for note in notes:
            pattern = r'\b' + re.escape(note.title) + r'\b'
            link = f'<a href="/note/{note.id}/" style="color:#38bdf8;">{note.title}</a>'
            content = re.sub(pattern, link, content)

        return mark_safe(content)

    # 🏷️ TAG SYSTEM
    def get_tags(self):
        return re.findall(r"#(\w+)", self.content)