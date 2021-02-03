# async-apscheduler-fastapi

Example of FastAPI service using an APScheduler to copy files locally. The same
concept can be used to copy files to/from AWS S3 buckets and such.

FastAPI uses the event loop provided by Uvicorn (uvloop), which is probably the
fastest implementation. Setting up the FastAPI service can't be easier.

APScheduler can use the same event loop to run jobs at specific intervals or
frequencies. The code here schedules a single job that runs every 5 seconds.

The scheduled job checks whether there are new files in an input directory.
If there are new files the job will put them in a asyncio Queue and will
schedule a few asyncio tasks to copy them to another directory and
delete them from the input directory.

The copy and delete file operations are done in an async executor, as the
function uses sync code.

The code must run in a single process, as otherwise there would be more than
one process looking for files in the input directory, which would lead to a
race condition.

