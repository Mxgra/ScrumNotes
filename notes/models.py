from django.db import models
from django.utils import timezone

# Create your models here.

#ToDo: Skipped Admin Tutorial

class Note(models.Model):
    note_text = models.CharField(max_length=500)
    pub_date = models.DateField('date published')
    do_date = models.DateField('date when the note is worked on', default=pub_date)
    done_date = models.DateField('date when the note is finished', default=pub_date)
    progress = models.IntegerField('note progress: 0 ToDo, 1 Doing, 2 Done', default=0)
    ended = models.BooleanField('note has already be counted as done note for the color grid', default=False)
    description = models.CharField(max_length=500, default="Here coud be your description!")

    def __str__(self):
        return self.note_text + " added at " + str(self.pub_date) + " with id: " + str(self.id)
    


def create_note(note_text):
    date = timezone.now().date()
    note = Note(note_text=note_text, pub_date=date, do_date=date, done_date=date)
    note.save()
    return note

class ColorGrid(models.Model):
    """
    Workflow as follows:
    1. User calls start_day via a button on the site
    2. User calls end_day via a button on the site
    3. When end_day is called, calc_progress is also called
    """
    date = models.DateField('date', unique=True)
    day_has_started = models.BooleanField(default=False)
    day_started = models.IntegerField('number of notes day started with', default=0)
    day_ended = models.IntegerField('number of notes day ended with', default=0)
    progress = models.IntegerField('day progress', default=0)

    def __str__(self):
        return str(self.date) + " progress: " + str(self.progress)
    
    def start_day(self):
        n_notes_todo = len(list(Note.objects.filter(progress=0)))
        self.day_started = n_notes_todo
        self.day_has_started
        self.save()
    
    def end_day(self):
        notes_done = list(Note.objects.filter(progress=2, ended=False))
        self.day_ended = len(notes_done)
        self.calc_progress()
        self.save()

        # Set ended value for all notes to true, to prevent counting them multiple times
        for note in notes_done:
            note.ended = True
            note.save()

    def calc_progress(self):
        if self.day_started == 0: self.day_started = 1
        #self.progress = self.progress + int(self.day_ended/self.day_started * 100)
        
        # Following implementations calculates the progress based on fixed numbers per note
        # e.g.: note_value=25: One needs to do 4 notes per day to have a green day, 2 for a yellow one
        # implementation of the colors is currently done inside the view itself. Make sure to change it there!
        note_value = 25
        self.progress += note_value * self.day_ended

