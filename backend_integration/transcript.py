from scraper_json import scrap_from_adv_rep
import json

transcriptPath = "test/OSR_ADVISING_HL.pdf"
with open(transcriptPath, "rb") as file:
    pdf_bytes = file.read()

transcript = scrap_from_adv_rep(pdf_bytes)

jsonTranscript = json.dumps(transcript, indent=2)
print(jsonTranscript)
