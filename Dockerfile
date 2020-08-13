FROM python:3

RUN mkdir -p /app
COPY requirements.txt /app
COPY src /app/src

WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP src/app
ENV FLASK_ENV production
EXPOSE 5000

ENTRYPOINT ["flask"]
CMD ["run"]
