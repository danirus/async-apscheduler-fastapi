# async-apscheduler-fastapi

Example of FastAPI service using an APScheduler to copy files locally. The same
concept can be used to copy files to/from AWS S3 buckets and such.

FastAPI uses the event loop provided by Uvicorn (uvloop), which is probably the
fastest implementation. Setting up the FastAPI service can't be easier.

The APScheduler package offers the `AsyncIOScheduler` that runs jobs in the same event loop used by FastAPI/Starlette. The example code here schedules a single job that runs every 5 seconds.

The scheduled job checks whether there are new files in the input directory,
`data/inbox`. If there are new files the job will put them in a asyncio Queue
and will schedule 3 asyncio tasks to copy them to another directory and
delete them from the input directory.

The copy and delete file operations are done in an async executor, as the
function that copies and deletes files use sync code.

This example code must run in a single process, as otherwise there would be
more than one process looking for files in the input directory, which would
lead to a race condition. However the file processing uses the pseudo-
parallelism offered by asyncio, which gives fast copy ratios.

## See it in action

Create a virtualenv, enable it and `pip install -r requirements.txt`.

Launch the service locally with `python run_service.py`.

You will see a log like the following in stdout:

    INFO:     Started server process [13242]
    INFO:     Waiting for application startup.
    INFO 2021-02-03 13:24:13,701 main Starting scheduler service.
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://localhost:8010 (Press CTRL+C to quit)
    INFO 2021-02-03 13:24:18,780 main I'm checking the inbox dir for files to process.
    INFO 2021-02-03 13:24:18,780 main I checked all the files in the inbox directory.
    INFO 2021-02-03 13:24:23,780 main I'm checking the inbox dir for files to process.
    INFO 2021-02-03 13:24:23,780 main I checked all the files in the inbox directory.

Visit the `app/main.py` module and see that the last 4 messages in the log come
from the job `SchedulerService.check_inbox_dir`, called every 5 seconds.

In order to feed the inbox directory with input files, run the script
`create_fake_files` and pass an argument 0. The script will create 10 files
with names from `file_00_0.csv` to `file_00_9.csv`. Calling the script with an
argument 1 will create files with prefix `file_01_?.csv`.

    $ python create_fake_files 0

After creating the 10 files the logs should display the following output:

    INFO 2021-02-03 13:24:28,778 main I'm checking the inbox dir for files to process.
    INFO 2021-02-03 13:24:28,778 main I checked all the files in the inbox directory.
    INFO 2021-02-03 13:24:33,780 main I'm checking the inbox dir for files to process.
    INFO 2021-02-03 13:24:35,782 main Queueing file_00_7.csv.
    INFO 2021-02-03 13:24:37,787 main Queueing file_00_6.csv.
    Execution of job "SchedulerService.check_inbox_dir (trigger: interval[0:00:05], next run at: 2021-02-03 13:24:38 CET)" skipped: maximum number of running instances reached (1)
    INFO 2021-02-03 13:24:39,788 main Queueing file_00_4.csv.
    INFO 2021-02-03 13:24:41,788 main Queueing file_00_5.csv.
    Execution of job "SchedulerService.check_inbox_dir (trigger: interval[0:00:05], next run at: 2021-02-03 13:24:43 CET)" skipped: maximum number of running instances reached (1)
    INFO 2021-02-03 13:24:43,791 main Queueing file_00_1.csv.
    INFO 2021-02-03 13:24:45,794 main Queueing file_00_0.csv.
    INFO 2021-02-03 13:24:47,795 main Queueing file_00_2.csv.
    Execution of job "SchedulerService.check_inbox_dir (trigger: interval[0:00:05], next run at: 2021-02-03 13:24:48 CET)" skipped: maximum number of running instances reached (1)
    INFO 2021-02-03 13:24:49,797 main Queueing file_00_3.csv.
    INFO 2021-02-03 13:24:51,800 main Queueing file_00_8.csv.
    INFO 2021-02-03 13:24:51,800 main I checked all the files in the inbox directory.
    INFO 2021-02-03 13:24:51,801 main I'm going to process file_00_7.csv...
    INFO 2021-02-03 13:24:51,801 main I'm going to process file_00_6.csv...
    INFO 2021-02-03 13:24:51,802 main I'm going to process file_00_4.csv...
    INFO 2021-02-03 13:24:51,815 main File file_00_6.csv has been processed in 2 seconds.
    INFO 2021-02-03 13:24:51,815 main I'm going to process file_00_5.csv...
    INFO 2021-02-03 13:24:51,817 main File file_00_7.csv has been processed in 2 seconds.
    INFO 2021-02-03 13:24:51,817 main I'm going to process file_00_1.csv...
    INFO 2021-02-03 13:24:51,817 main File file_00_4.csv has been processed in 2 seconds.
    INFO 2021-02-03 13:24:51,817 main I'm going to process file_00_0.csv...
    INFO 2021-02-03 13:24:51,821 main File file_00_5.csv has been processed in 2 seconds.
    INFO 2021-02-03 13:24:51,822 main I'm going to process file_00_2.csv...
    INFO 2021-02-03 13:24:51,823 main File file_00_0.csv has been processed in 2 seconds.
    INFO 2021-02-03 13:24:51,823 main I'm going to process file_00_3.csv...
    INFO 2021-02-03 13:24:51,824 main File file_00_1.csv has been processed in 2 seconds.
    INFO 2021-02-03 13:24:51,824 main I'm going to process file_00_8.csv...
    INFO 2021-02-03 13:24:51,828 main File file_00_2.csv has been processed in 2 seconds.
    INFO 2021-02-03 13:24:51,830 main File file_00_3.csv has been processed in 2 seconds.
    INFO 2021-02-03 13:24:51,831 main File file_00_8.csv has been processed in 2 seconds.
    INFO 2021-02-03 13:24:53,776 main I'm checking the inbox dir for files to process.
    INFO 2021-02-03 13:24:53,776 main I checked all the files in the inbox directory.
    INFO 2021-02-03 13:24:58,776 main I'm checking the inbox dir for files to process.
    INFO 2021-02-03 13:24:58,776 main I checked all the files in the inbox directory.
    INFO 2021-02-03 13:25:03,779 main I'm checking the inbox dir for files to process.
    INFO 2021-02-03 13:25:03,779 main I checked all the files in the inbox directory.
    ^CINFO:     Shutting down
    INFO:     Waiting for application shutdown.
    INFO:     Application shutdown complete.

The `asyncio.sleep(2)` in the scheduled job makes the APScheduler hold on the
next interval, as the previous job didn't finish yet. And we want only 1
instance of this job: `max_instances=1`.