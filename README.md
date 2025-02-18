# KnowledgeSysCapstone

To create a venv environment to run your project, run the following command:

```sh
python -m venv capstone
```

To activate your python enviornment, please run the following command:

```sh
capstone\Scripts\activate
```

To add environment to your workspace run:

```sh
pip install -r requirements.txt

```

Please create your local env to look like the following:

```sh
ELASTIC_PASSWORD=BLAHBLAHBLAH
```

Elasticsearch Docker tutorial: https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

To get elasticsearch functionality to work, please save the http_ca.crt certificate to the KnowledgeSysCapstone folder by:

1. Clicking on you container in Docker Desktop
2. Going to your files
3. Left click on usr/share/elasticsearch/config/certs/http_ca.crt in files for your container and save that to your local project folder.
