from django.test import TestCase
from .models import Note, ColorGrid, create_note
from django.utils import timezone

# Create your tests here.
class ColorGridTestCase(TestCase):
    color_grid = None
    test_notes = None
    

    def setUp(self) -> None:
        self.test_notes = [create_note("This is the {} test".format(i)) for i in range(10)]
        #print(self.test_notes)
        self.color_grid = ColorGrid(date=timezone.now().date())
        #return super().setUp()
    
    def test_start_day(self):
        self.color_grid.start_day()
        n_day_started = self.color_grid.day_started
        self.assertEqual(n_day_started, len(self.test_notes))

    def test_end_day(self):
        notes = Note.objects.all()
        for i, note in enumerate(notes):
            if i==5: break

            note.progress = 2
            note.save()

        self.color_grid.end_day()
        n_day_ended = self.color_grid.day_ended
        self.assertEqual(n_day_ended, 5)

    def test_calc_progress(self):
        self.color_grid.start_day()

        # User now works on the todos:
        notes = Note.objects.all()
        for i, note in enumerate(notes):
            if i==5: break

            note.progress = 2
            note.save()
        
        self.color_grid.end_day()
        self.color_grid.calc_progress()
        self.assertEqual(self.color_grid.progress, 50)
