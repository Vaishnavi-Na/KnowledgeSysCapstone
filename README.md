# KnowledgeSysCapstone

## Virtual Environment

If a venv enviroment not created in your project, run the following command:
`python -m venv <foldername>`
for example

```sh
python -m venv capstone
# or
python -m venv .venv
```

To activate your python enviornment, please run the following command:
`<foldername>\Scripts\activate`
for example

```sh
capstone\Scripts\activate
# or
.\venv\Scripts\activate

# on Linux/MacOS, 
source venv/bin/activate
```

To add environment to your workspace run:

```sh
pip install -r requirements.txt
```

Please create your local env to look like the following:

```sh
ELASTIC_PASSWORD=BLAHBLAHBLAH
```

Elasticsearch Docker tutorial: <https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html>

To get elasticsearch functionality to work, please save the http_ca.crt certificate to the KnowledgeSysCapstone folder by:

1. Clicking on you container in Docker Desktop
2. Going to your files
3. Left click on usr/share/elasticsearch/config/certs/http_ca.crt in files for your container and save that to your local project folder.

## FastAPI backend

[WARN] This section is generated, to modify, please go to the backend_integration\README.md

To test & Run Locally, first cd to the folder:

```bash
cd .\backend_integration\
```

Then run command

```bash
fastapi dev main.py
```

## coursesearchplus

[WARN] This section is generated, to modify, please go to the coursesearchplus\README.md

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

### Getting Started

cd to coursesearchplus folder

```bash
cd ./coursesearchplus/
```

If npm not installed, run:

```bash
npm install
```

If next.js not installed, run:

```bash
npm install next
```

First, run the development server:

```bash
npm run dev
## or
yarn dev
## or
pnpm dev
## or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

### Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

### Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
