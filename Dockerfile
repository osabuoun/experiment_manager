FROM python:3

ADD requirements.txt /experiment_manager/requirements.txt
ADD experiment.py /experiment_manager/experiment.py
ADD docker_agent.py /experiment_manager/docker_agent.py
ADD prometheus_getter.py /experiment_manager/prometheus_getter.py
ADD time_decoder.py /experiment_manager/time_decoder.py
ADD job_manager.py /experiment_manager/job_manager.py
ADD jqueuing_worker.py /experiment_manager/jqueuing_worker.py
ADD job_operations.py /experiment_manager/job_operations.py
ADD experiment_manager.py /experiment_manager/experiment_manager.py
ADD parameters.py /experiment_manager/parameters.py
ADD monitoring.py /experiment_manager/monitoring.py
ADD index.html /experiment_manager/index.html
WORKDIR /experiment_manager/
RUN mkdir log
RUN mkdir data
RUN pip install -r requirements.txt
RUN pip install -U "celery[redis]"
ENTRYPOINT python3 experiment_manager.py 