from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from django.db.utils import IntegrityError

from .models import Note, create_note, ColorGrid
from .form import AddNoteForm, MoveNoteForm

# Create your views here.


def index(request):
    
    #ToDo: add start/end day buttons
    notes_todo = Note.objects.filter(progress=0)
    notes_doing = Note.objects.filter(progress=1)
    notes_done = Note.objects.filter(progress=2)
    
    grid = ColorGrid.objects.all()
    weeks = {}
    week = 0

    # ToDo: Missing date functionality: Right now it places the values of Cologrid
    # not regarding the actual weekdays. It should ofcourse check to which day (e.g Tuesday)
    # the date belongs, and then place that inside the correct grid element
    for i, day in enumerate(grid):
        if i%7 == 0:
            week += 1
        if week in weeks:
            weeks[week].append(day.progress)
        else:
            weeks[week] = [day.progress]

    context = {
        'notes_todo': notes_todo,
        'notes_doing': notes_doing,
        'notes_done': notes_done,
        'weeks': weeks
    }
    
    return render(request, 'notes/index2.html', context)

def detail(request, note_id):
    n = Note.objects.get(id=note_id)
    context = {'note_id': note_id,
               'description': n.description}
    return render(request, 'notes/details.html', context)

def add_note(request):
    return render(request, 'notes/add_note.html')
    

def note_added(request):
    
    if request.method == 'POST':
        
        # create a form instance and populate it with data from the request:
        form = AddNoteForm(request.POST)
        #print(form)
        if form.is_valid():
            #print('Here')
            # ToDo: check if note is non-empty
            note_text = form.cleaned_data['note']
            note = create_note(note_text)
            print(note)

            return redirect('index')
            #return render(request, 'notes/index.html')

    else:
        form = AddNoteForm()
    # this redirects to index
    return redirect('index')
    #return render(request, 'notes/index.html')

def move_note(request):
    print('here')
    move_right = False
    if 'move_right_btn' in request.POST:
        note_id = request.POST['move_right_btn']
        move_right = True
    elif 'move_left_btn' in request.POST:
        note_id = request.POST['move_left_btn']
        #move_left = True
    elif 'delete' in request.POST:
        # ToDo: this should obviously be in its own function
        note_id = request.POST['delete']
        note = Note.objects.get(id=note_id)
        note.delete()
        return redirect('index')
    
    
    note = Note.objects.get(id=note_id)
    if move_right:
        note.progress += 1
    else:
        note.progress -= 1

    if note.progress == 3:
        # ToDo: Really delete? or save for history?
        note.delete()
    note.save()
    print(note)
    return redirect('index')
    
def safe_description(request, note_id):
    
    n = Note.objects.get(id=note_id)
    current = n.description
    
    if request.POST['editDescription'] != current:
        
        n.description = request.POST['editDescription']
        n.save()
    
    context = {'note_id': note_id,
               'description': n.description}
    return render(request, 'notes/details.html', context)

def start_day(request):
    date = timezone.now().date()
    try:
        day = ColorGrid(date=date)
        day.start_day()
    except IntegrityError as e:
        print("Error was caught, there cannot exist multiple entries of the same date\n", e)

    return redirect('index')

def end_day(request):
    # ToDo: What happens if the user forgets to end a day?
    # maybe add "end previous day"-button? Or remove all dates, simply go with ids.
    date = timezone.now().date()
    #day = ColorGrid.objects.get(date=date)

    try:
    # with this, if the user forgets to end a day, he can still end it the next time
    # he logs in, as end day will always end the last day in the db
        day = ColorGrid.objects.latest('date')
        print('ended day:', day)
        day.end_day()

        notes_done = Note.objects.filter(progress=1)
        for note in notes_done:
            note.progress = 0
            note.save()

    except ColorGrid.DoesNotExist:
        # Handle case where no entries exist in the database
        day = None
    

    return redirect('index')

def clear_day(request):
    # ToDO: What if clead day is accidentally invoked before end_day? progress lost
    notes_done = Note.objects.filter(progress=2)
    for note in notes_done:
        note.progress = 3
        note.save()
        #note.delete()
    return redirect('index')