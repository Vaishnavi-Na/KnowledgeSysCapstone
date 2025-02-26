import re
import pdfplumber

def scrap_from_adv_rep(path) -> dict:
    '''Scrap the specialization info and courses taken from the OSU advising report.

    Argument:
        path: The path to the input OSU advising report
    Return: 
        A dict with one entry "specialization":"SPL" and one entry "courses_taken": A set of str.
    '''
    result = {
        "specialization": "",
        "courses_taken": set()
    }

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            SUMMARY_BBOX = (0, page.height * 0.12, page.width * 0.30, page.height)
            # SUMMARY = page.within_bbox(SUMMARY_BBOX).extract_table()
            SUMMARY = page.within_bbox(SUMMARY_BBOX).extract_text()
            # print(SUMMARY)
            SUMMARY = SUMMARY.split("TEST RESULTS")[0]

            # Search for the last occurrence
            spl = re.findall(r'UENG SPL (\w{3})', SUMMARY)[-1]
            # print(f"[DEBUG] {spl}")

            result["specialization"] = spl if spl else "Not Found"
            # f.write(SUMMARY+"\n\n")

            COURSES = ""
            COURSES1_BBOX = (
                page.width * 0.32, page.height * 0.12, 
                page.width * 0.55, page.height * 0.90
            )
            COURSES += page.within_bbox(COURSES1_BBOX).extract_text()

            COURSES2_BBOX = (
                page.width * 0.54, page.height * 0.12, 
                page.width * 0.78, page.height * 0.90
            )
            COURSES += page.within_bbox(COURSES2_BBOX).extract_text()

            COURSES3_BBOX = (
                page.width * 0.77, page.height * 0.12, 
                page.width * 1.00, page.height * 0.90
            )
            COURSES += page.within_bbox(COURSES3_BBOX).extract_text()

            courses_pattern = r"^(?!.*UENG$)([A-Z]+(?:\s?[A-Z]+)?\s\d{4})"

            # Find all matches
            result["courses_taken"] = re.findall(courses_pattern, COURSES, re.MULTILINE)
    return result


# Print the scrap result for test
print(str(scrap_from_adv_rep("adv_rep_scraper\\test\\OSR_ADVISING_NV.pdf")))