FROM python:3.8
ENV VENV=/opt/venv
RUN python3 -m venv $VENV && \
    apt-get update && \
    apt-get install ffmpeg libsm6 libxext6 -y
ENV PATH="$VENV/bin:$PATH"
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
COPY ./src/ /code/src/
CMD python src/app.py
