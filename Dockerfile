# 
FROM python:3.9

# Install OpenGL
RUN apt-get update && apt-get install -y \
  libgl1-mesa-glx \
  && rm -rf /var/lib/apt/lists/*

# 
WORKDIR /

# 
COPY ./requirements.txt /requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# 
COPY ./ /

# 

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]