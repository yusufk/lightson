# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./lightson /code/lightson

#
EXPOSE 80 
CMD ["dapr","run","--app-id","lightson","--","uvicorn","lightson.main:app", "--host", "0.0.0.0", "--port", "80"]