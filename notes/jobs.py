from schedule import Scheduler
import threading
from time import sleep, strftime, gmtime
from .views import end_day

# Taken from: https://stackoverflow.com/questions/44896618/django-run-a-function-every-x-seconds

def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        self.name = "BLABLABKA"
        print(self.name)
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                sleep(interval)
            
        def __exit__(self, exec_type, exc_value, traceback):
            # if the jobs are not stop, you can stop them
            self._job_stop.set()
            print("Stopped bg jobs...hopefully")

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True) # this closes the bg thread when main thread is exited
    continuous_thread.start()
    return cease_continuous_run

def end_day_job():
    print("Executing end_day_job()... checking for time.")
    if int(strftime("%H", gmtime())) >= 22:
        print("called end_day...")
        end_day()


Scheduler.run_continuously = run_continuously

def start_scheduler():
    scheduler = Scheduler()
    scheduler.every().hour.do(end_day_job)
    scheduler.run_continuously()
