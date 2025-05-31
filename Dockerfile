FROM public.ecr.aws/lambda/python:3.10

RUN pip install poetry==1.8.3

ENV PYTHONPATH=${PYTHONPATH}:src

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERE=1
ENV PIP_DEFAULT_TIMEOUT=60

COPY dist /app/dist

RUN pip install --upgrade pip
RUN pip install /app/dist/*.whl
RUN ls -la

COPY src/* ${LAMBDA_TASK_ROOT}

CMD [ "review_extractor.main.handler" ]
