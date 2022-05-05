FROM python:3.10
COPY . .
RUN pip install --user -r requirements.txt
CMD [ "python" , "./main.py"]