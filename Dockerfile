FROM public.ecr.aws/lambda/python:3.9

COPY lambda_function.py ${LAMBDA_TASK_ROOT}
RUN pip install boto3

CMD ["lambda_function.lambda_handler"]

