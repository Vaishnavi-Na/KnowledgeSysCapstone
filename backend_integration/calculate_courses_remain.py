
import json

with open("major_curriculum.json") as f:
    major_curriculum: dict = json.load(f)

with open("osu_cse_courses.json") as f:
    prereq_info: list[dict] = json.load(f)
    # print(prereq_info[0]["course"])

def calculate_remaining_courses(transcript: dict) -> dict:
    taken_courses: set[str] = set(transcript['courses'])
    specialization: str = transcript.get('special', '')
    # Test: {"special": "AIT", "courses": []}
    # {"special": "AIT", "courses": ["Math 2568", "CSE 2331", "Stat 3201"]}

    # Combine general and specialization-specific courses
    curriculum: list[str] = list(major_curriculum["general"])
    curriculum.extend(major_curriculum.get(specialization, []))

    remaining_courses = set()
    unmet_prereqs = {}

    def check_course_prereqs(course: str):
        if course in taken_courses:
            return []  # already completed, no unmet prereqs

        # Find prerequisite info
        course_reqs = next((item["prereqs"] for item in prereq_info if item["course"] == course), None)
        if not course_reqs:
            return []  # no prerequisites, course can be taken

        unmet_groups = []
        all_requirements = course_reqs.get('Prerequisites', []) + course_reqs.get('Concurrent Courses', [])

        for prereq_group in all_requirements:
            # At least one course in the group must be taken
            if not any(c in taken_courses for c in prereq_group):
                unmet_groups.append(prereq_group)

        return unmet_groups

    for course in curriculum:
        unmet_groups = check_course_prereqs(course)
        if not unmet_groups:
            remaining_courses.add(course)
        else:
            unmet_prereqs[course] = unmet_groups

    # You can return both remaining_courses and unmet_prereqs if needed:
    return {
        "cantake": sorted(remaining_courses - taken_courses), 
        "unmet_prereq": unmet_prereqs
    }