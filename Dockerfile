FROM python:3.10

# set the working directory
WORKDIR /app

COPY requirements.txt /app/

# install dependencies
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 5000

# run the application
CMD ["flask", "run", "--host=0.0.0.0"]