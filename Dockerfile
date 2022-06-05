FROM python:latest
 
WORKDIR /thebott
COPY . /thebott
 
RUN pip install -r requirements.txt
 
ENTRYPOINT ["python"]
CMD ["bot.py"]
