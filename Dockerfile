FROM python:3

ADD requirements.txt /experiment_manager/requirements.txt
ADD experiment_operations.py /experiment_manager/experiment_operations.py
ADD experiment_manager.py /experiment_manager/experiment_manager.py
ADD config /experiment_manager/config
ADD data /experiment_manager/data
ADD monitoring.py /experiment_manager/monitoring.py
WORKDIR /experiment_manager/
RUN pip install -r requirements.txt
RUN pip install -U "celery[redis]"
ENTRYPOINT python3 experiment_manager.py 