FROM python:3.7.2-alpine3.8

LABEL maintainer="Miguel Contreras <migueldevelop@gmail.com>"

WORKDIR /usr/src/app/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN behave
RUN rm -rf ./input/* ./output/* ./backup/*

VOLUME [ "/usr/src/app/input", "/usr/src/app/output", "/usr/src/app/backup" ]

ARG UID=1000
ARG GID=1000
USER $UID:$GID

ENTRYPOINT [ "python",  "./run.py" ]