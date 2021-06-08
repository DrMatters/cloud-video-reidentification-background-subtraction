FROM continuumio/miniconda3:4.7.10

COPY conda.txt .
RUN conda install --yes --file conda.txt \
    && conda clean -afy

COPY requirements.txt .
RUN pip install --user -r requirements.txt \
    && rm -rf ~/.cache

WORKDIR /opt/deep_moderator_worker
COPY . .

ENV GOOGLE_APPLICATION_CREDENTIALS=/root/gcloud.json

CMD ["python", "main.py"]
