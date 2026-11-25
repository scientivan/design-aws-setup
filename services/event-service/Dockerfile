FROM public.ecr.aws/docker/library/python:3.12-alpine
WORKDIR /app
COPY app.py .
ENV PORT=8081
EXPOSE 8081
USER nobody
CMD ["python", "-u", "app.py"]
