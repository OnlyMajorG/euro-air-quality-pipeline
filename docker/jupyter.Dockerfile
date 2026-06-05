FROM python:3.10-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

COPY docker/requirements-docker.txt /tmp/requirements-docker.txt
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements-docker.txt \
    && mkdir -p /workspace /root/.ivy2

RUN python3 -m ipykernel install --sys-prefix --name euro-air-quality --display-name "Euro Air Quality"

WORKDIR /workspace

EXPOSE 8888

CMD ["python3", "-m", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--IdentityProvider.token=", "--ServerApp.password="]
