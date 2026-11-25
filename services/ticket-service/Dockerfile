FROM public.ecr.aws/docker/library/python:3.12-alpine
WORKDIR /app
COPY app.py .
ENV PORT=8082
EXPOSE 8082
USER nobody
CMD ["python", "-u", "app.py"]
