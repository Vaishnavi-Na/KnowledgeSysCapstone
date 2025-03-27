import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from dotenv import load_dotenv
import ssl
import os
from elasticsearch import Elasticsearch


url = "https://osu.bluera.com/osubpi/fbview-WebService.asmx/getFbvGrid"

subjects = [
    "ACADAFF", "ACCAD", "ACCTMIS", "ACEL", "AEDECON", "AEE", "AEROENG", "AFAMAST", 
    "AGRCOMM", "AGSYSMT", "AIRSCI", "ANATOMY", "ANIMSCI", "ANMLTEC", "ANTHROP", 
    "ARABIC", "ARCH", "ART", "ARTEDUC", "ARTSSCI", "ASE", "ASL", "ASTRON", "ATHTRNG", 
    "ATMOSSC", "AVIATN", "BCS", "BIOCHEM", "BIOETHC", "BIOLOGY", "BIOMEDE", "BIOMSCI", 
    "BIOPHRM", "BIOPHYS", "BIOTECH", "BMI", "BSGP", "BUSADM", "BUSFIN", "BUSMGT", 
    "BUSMHR", "BUSML", "BUSOBA", "BUSTEC", "CBE", "CBG", "CHEM", "CHEMPHY", "CHINESE", 
    "CIVILEN", "CLAS", "CLLC", "COMLDR", "COMM", "COMPSTD", "CONSCI", "CONSYSM", 
    "CRPLAN", "CRPSOIL", "CSCFFS", "CSE", "CSFRST", "CSHSPMG", "DANCE", "DENT", 
    "DENTHYG", "DESIGN", "DSABLST", "EALL", "EARTHSC", "ECE", "ECON", "EDUCST", 
    "EDUTL", "EEOB", "EEURLL", "EHE", "ENGLISH", "ENGR", "ENGREDU", "ENGRTEC", 
    "ENGTECH", "ENR", "ENTMLGY", "ENVENG", "ENVSCI", "ENVSCT", "ESCE", "ESEADM", 
    "ESEPOL", "ESEPSY", "ESHESA", "ESLTECH", "ESPHE", "ESQREM", "ESQUAL", "ESSPED", 
    "ESSPSY", "ESTEPL", "ESWDE", "EXP", "FABENG", "FAES", "FDSCTE", "FILMSTD", 
    "FRENCH", "FRIT", "GENBIOL", "GENCHEM", "GENCOMM", "GENHUM", "GENMATH", "GENSSC", 
    "GENSTDS", "GEOG", "GEOSCIM", "GERMAN", "GRADSCH", "GRADTDA", "GREEK", "HCINNOV", 
    "HCS", "HDFS", "HEBREW", "HIMS", "HINDI", "HISTART", "HISTORY", "HONORS", 
    "HORTTEC", "HTHRHSC", "HUMNNTR", "HWIH", "INTMED", "INTSTDS", "ISE", "ITALIAN", 
    "JAPANSE", "JEWSHST", "KINESIO", "KNHES", "KNPE", "KNSFHP", "KNSISM", "KOREAN", 
    "LARCH", "LATIN", "LING", "MATH", "MATSCEN", "MBA", "MCDBIO", "MDN", "MDRNGRK", 
    "MEATSCI", "MECHENG", "MEDCOLL", "MEDDIET", "MEDLBS", "MEDMCIM", "MEDREN", 
    "MICRBIO", "MILSCI", "MOLGEN", "MUSIC", "MVNGIMG", "NAVALSC", "NELC", "NEUROGS", 
    "NEUROSC", "NEURSGY", "NRSADVN", "NRSPRCT", "NUCLREN", "NURSING", "OCCTHER", 
    "OSBP", "PATHOL", "PERSIAN", "PHILOS", "PHR", "PHYSICS", "PHYSIO", "PHYSTHR", 
    "PLNTPTH", "POLISH", "POLITSC", "PORTGSE", "PSYCH", "PUBAFRS", "PUBHBIO", 
    "PUBHEHS", "PUBHEPI", "PUBHHBP", "PUBHHMP", "PUBHLTH", "QUECHUA", "RADSCI", 
    "RELSTDS", "RESPTHR", "ROMANIA", "ROMLING", "RURLSOC", "RUSSIAN", "SANSKRT", 
    "SCANDVN", "SCHOLAR", "SLAVIC", "SOCIOL", "SOCWORK", "SOMALI", "SPANISH", 
    "SPHHRNG", "STAT", "SWAHILI", "SWEDISH", "SXLTYST", "TECPHYS", "THEATRE", 
    "TURKISH", "VETBIOS", "VETCLIN", "VETPREV", "WELDENG", "WGSST", "YIDDISH"
]
all_data = []

session = requests.Session()

headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Accept": "*/*",
    "Origin": "https://osu.bluera.com",
    "Referer": "https://osu.bluera.com/osubpi/fbview.aspx?blockid=GZZtwnsmMT3Du&lng=en",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15",
    "X-Requested-With": "XMLHttpRequest"
}

#Elasticsearch setup
ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

def updateIndex(name, professor):
    # Search for: professor with matching last and first name
    query = {
        "query": {
            "bool":{
                "must": [
                    {"match": {"lastName": name["lastName"] }},
                    {"match": {"firstName": name["firstName"]}}
                ]
            }
        }
    }
    es.indices.refresh(index="professors")
    res = es.search(index='professors', body=query)

    # If no entry for the professor currently exists, add to index
    if not res["hits"]["hits"]: 
        name["SEI"] = [professor]
        print("\nProfessor not found: ", name["lastName"] + name["firstName"])
        es.index(index='professors', id=name["lastName"] + name["firstName"], document=name)
        print(name)
    # Else append to current professor index
    else:
        # Get the doc for the professor
        doc = res["hits"]["hits"][0]
        source = doc['_source']
        docID = doc['_id']

        print("\n appending: " + name["lastName"] + name["firstName"])

        # If there are currently no SEI entries, add to doc
        # Append the new SEI review to the professor SEI entries
        if "SEI" not in source:
            source["SEI"] = [professor]
            print("\nSEI not in source")         
        else: source["SEI"].append(professor)    

        # Update the elasticsearch index 
        es.index(index='professors', id=docID, document=source)
        
    return

for subject in subjects:
    print(f"scraping: {subject}...")

    page = 1  
    retry = 0  
    while True:
        payload = {
            "strUiCultureIn": "en",
            "datasourceId": "3310",  
            "blockId": "730",  
            "subjectColId": "0",
            "subjectValue": subject,
            "detailValue": "-1",
            "gridId": "fbvGridDrilldown",
            "pageActuelle": page,  
            "strOrderBy": ["col_3", "asc", subject, ""],
            "strFilter": ["", "", "ddlFbvColumnSelector", ""],
            "sortCallbackFunc": "__getFbvGridDrilldownData",
            "userid": "",
            "pageSize": "100"
        }

        try:
            response = session.post(url, json=payload, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f" request fail: {response.status_code}")
                print("sever return:", response.text)
                retry += 1
                if retry >= 3:  
                    print(f" {subject} skip...")
                    break
                time.sleep(1)
                continue

            data = response.json()

            if "d" not in data:
                break

            html_content = data["d"][0]
            soup = BeautifulSoup(html_content, "html.parser")
            rows = soup.find_all("tr", class_="gData")

            for row in rows:
                cols = row.find_all("td")
                if len(cols) < 14:  
                    print(f"⚠️ Skipping row with insufficient columns in subject {subject}")
                    continue  
                name = {
                    "lastName": cols[0].text.strip(),
                    "firstName": cols[1].text.strip(),
                }
                professor = {
                    "Subject": cols[2].text.strip(),
                    "Catalog": cols[3].text.strip(),
                    "Class Name": cols[4].text.strip(),
                    "Class Number": cols[5].text.strip(),
                    "Term": cols[6].text.strip(),
                    "College": cols[7].text.strip(),
                    "Department": cols[8].text.strip(),
                    "Medium": cols[9].text.strip(),
                    "Campus": cols[10].text.strip(),
                    "Class Size": cols[11].text.strip(),
                    "Responses": cols[12].text.strip(),
                    "Rating": cols[13].text.strip(),
                }
                print("\nNew entry----------------------------------")
                updateIndex(name, professor)
                all_data.append(professor)

            print(f"finish {subject}  {page} ，total {len(rows)} datas")
            if not rows:
                print(f" No data found for subject {subject}, skipping...")
                break  # Skip this subject and continue to the next one

            if len(rows) < 20:
                break

            page += 1  
            time.sleep(1) 

        except requests.exceptions.RequestException as e:
            retry += 1
            if retry >= 3:
                print(f" {subject} skip...")
                break  
            time.sleep(1)

df = pd.DataFrame(all_data)
df.to_csv("osu_professors_data.csv", index=False, encoding="utf-8")
print("Done")