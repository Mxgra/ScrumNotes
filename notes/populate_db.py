from django.utils import timezone
from datetime import timedelta
from .models import Note, create_note, ColorGrid
import random

def main():
    #print('here')
    for i in range(1,18):
        #print("here")
        c = ColorGrid(date=timezone.now().date()-timedelta(days=i), progress= random.randrange(10, 100, 5))
        #print(c) 
        c.save()
        
    print(ColorGrid.objects.all())
    #print(self.test_notes)

if __name__ == "__main__":
    main()

