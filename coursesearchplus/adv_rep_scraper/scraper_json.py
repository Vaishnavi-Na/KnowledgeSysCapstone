import re
import pdfplumber # type: ignore
import sys
import json
import tempfile

def scrap_from_adv_rep(file) -> dict:
    '''Scrap the specialization info and courses taken from the OSU advising report.

    Argument:
        file: The pdf file
    Returns: 
        A dict with one entry "special":"SPL" and one entry "courses": A set of str.
    '''
    result = {
        "special": "",
        "courses": set()
    }

    try:
         # Create a temporary file to store the PDF data
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file)  # Write the byte data to the file
            temp_file_path = temp_file.name

        with pdfplumber.open(temp_file_path) as pdf:
            for page in pdf.pages:
                SUMMARY_BBOX = (0, page.height * 0.12, page.width * 0.30, page.height)
                # SUMMARY = page.within_bbox(SUMMARY_BBOX).extract_table()
                SUMMARY = page.within_bbox(SUMMARY_BBOX).extract_text()
                # print(SUMMARY)
                SUMMARY = SUMMARY.split("TEST RESULTS")[0]

                # Search for the last occurrence
                spl = re.findall(r'UENG SPL (\w{3})', SUMMARY)[-1]
                # print(f"[DEBUG] {spl}")

                result["special"] = spl if spl else "Not Found"
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
                result["courses"] = re.findall(courses_pattern, COURSES, re.MULTILINE)
    except Exception as e:
        result = {"error": str(e)}

    return result

# Read from stdin
file = sys.stdin.buffer.read()
result = scrap_from_adv_rep(file)

try:
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({"error": f"Error during JSON serialization: {str(e)}"}))
