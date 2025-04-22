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
.venv\Scripts\activate

# on Linux/MacOS,
source venv/bin/activate
```

To add environment to your workspace run:

```sh
pip install -r requirements.txt
```

## Setting up ElasticSearch
The main backend database we use on this project is ElasticSearch, which indexes and stores documents. It's used for sorting, and accessing all of the data we scrape. We host our ElasticSearch instances locally in Docker containers on our devices. To set it up please follow the directions below. 

Elasticsearch Docker tutorial: <https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html>

Please create your local .env to look like the following:

```sh
ELASTIC_PASSWORD=YourElasticSearchPassword
```

To get elasticsearch functionality to work, please save the http_ca.crt certificate to the KnowledgeSysCapstone folder by:

1. Clicking on you container in Docker Desktop
2. Going to your files
3. Left click on usr/share/elasticsearch/config/certs/http_ca.crt in files for your container and save that to your local project folder.

## Scraping Content

Before you can begin displaying your website, you need to first scrape all of the content necessary. This is the most time consuming process and as a result, we have already done some of it for you. In docker files, you will find all of the generated LLM summaries, SEI data, and class information for next semester that were generated. However, to get other data, you must run the below files:

1) next_fall_scraper.py: Uses selenium to scrape the information for the classes professors will teach next fall and the classes they have already taught before in the last academic year using data from the OSU Course Search website.
2) RMP_scraper.py: Uses RMP's GraphQL node to scrape Rate My Professor ratings for every single professor at OSU. This can be time-consuming, the type of program you run overnight.
3) SEIscraper.py: Uses Bluera, OSU's official SEI partner to scrape information on the SEI score of every professor at OSU in the last three academic year. This one is also time-consuming, if you don't want to spend all day, simply change the list of subjects to "CSE" or whatever subject you're focusing on and scrape that in a couple minutes instead. 

After this, you should be set to actual set up the website for display. 

## FastAPI backend
Whew, you're done! You just finished the hardest part. It's easy breezing from here. 

Because of Elastic Search, need to download or move `http_ca.crt` into `\backend_integration\` folder.

To test & Run Locally, first cd to the folder:

```bash
cd \backend_integration
```

Then run command

```bash
fastapi dev main.py
```

## Front End

Our front-end for this project is Next.js. To find documentation on how to run it, please follow the next.js documentation provided below:
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
