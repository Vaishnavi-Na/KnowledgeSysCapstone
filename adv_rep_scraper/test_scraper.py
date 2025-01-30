import pdfplumber

f = open("adv_rep_scraper/test_scrape_res.txt", "w")
with pdfplumber.open("adv_rep_scraper/OSR_ADVISING.pdf") as pdf:
    for page in pdf.pages:
        SUMMARY_BBOX = (0, page.height * 0.12, page.width * 0.30, page.height * 0.39)
        # SUMMARY = page.within_bbox(SUMMARY_BBOX).extract_table()
        SUMMARY = page.within_bbox(SUMMARY_BBOX).extract_text()
        # print(SUMMARY)
        f.write(SUMMARY+"\n\n")

        COURSES1_BBOX = (
            page.width * 0.30, page.height * 0.12, 
            page.width * 0.54, page.height * 0.90
        )
        COURSES1 = page.within_bbox(COURSES1_BBOX).extract_text()
        f.write(COURSES1+"\n")

        COURSES2_BBOX = (
            page.width * 0.54, page.height * 0.12, 
            page.width * 0.80, page.height * 0.90
        )
        COURSES2 = page.within_bbox(COURSES2_BBOX).extract_text()
        f.write(COURSES2+"\n")

f.close()
