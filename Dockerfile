FROM python:3
ADD cost.py /
RUN pip install pymesh
CMD [ "python", "./cost.py" ]
