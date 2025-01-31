import pdfplumber

# Input file
test_adv_rep = "OSR_ADVISING_NV"
f = open(f"adv_rep_scraper/test/test_res_{test_adv_rep}.txt", "w")

specialization = ""
courses_taken = {}
with pdfplumber.open(f"adv_rep_scraper/test/{test_adv_rep}.pdf") as pdf:
    for page in pdf.pages:
        SUMMARY_BBOX = (0, page.height * 0.12, page.width * 0.30, page.height)
        # SUMMARY = page.within_bbox(SUMMARY_BBOX).extract_table()
        SUMMARY = page.within_bbox(SUMMARY_BBOX).extract_text()
        # print(SUMMARY)
        SUMMARY = SUMMARY.split("TEST RESULTS")[0]
        f.write(SUMMARY+"\n\n")

        COURSES1_BBOX = (
            page.width * 0.32, page.height * 0.12, 
            page.width * 0.55, page.height * 0.90
        )
        COURSES1 = page.within_bbox(COURSES1_BBOX).extract_text()
        f.write(COURSES1+"\n")

        COURSES2_BBOX = (
            page.width * 0.54, page.height * 0.12, 
            page.width * 0.78, page.height * 0.90
        )
        COURSES2 = page.within_bbox(COURSES2_BBOX).extract_text()
        f.write(COURSES2+"\n")

        COURSES3_BBOX = (
            page.width * 0.77, page.height * 0.12, 
            page.width * 1.00, page.height * 0.90
        )
        COURSES3 = page.within_bbox(COURSES3_BBOX).extract_text()
        f.write(COURSES3+"\n")

f.close()
