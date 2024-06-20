FROM python:3.10

RUN echo 'alias ll="ls -al"' >> /root/.bashrc

COPY src /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["tail", "-f", "/dev/null"]
