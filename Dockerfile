FROM python:3

ADD requirements.txt /experiment_manager/requirements.txt
ADD experiment_operations.py /experiment_manager/experiment_operations.py
ADD job_manager.py /experiment_manager/job_manager.py
ADD jqueuing_worker.py /experiment_manager/jqueuing_worker.py
ADD job_operations.py /experiment_manager/job_operations.py
ADD experiment_manager.py /experiment_manager/experiment_manager.py
ADD parameters.py /experiment_manager/parameters.py
ADD monitoring.py /experiment_manager/monitoring.py
WORKDIR /experiment_manager/
RUN mkdir log
RUN mkdir data
RUN pip install -r requirements.txt
RUN pip install -U "celery[redis]"
ENTRYPOINT python3 experiment_manager.py 