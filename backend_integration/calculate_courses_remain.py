
import json

with open("major_curriculum.json") as f:
    major_curriculum: dict = json.load(f)

with open("prereq_info.json") as f:
    prereq_info: dict = json.load(f)

def calculate_remaining_courses(transcript: dict) -> list[str]:
    taken_courses: set[str] = set(transcript['courses'])
    specialization: str = transcript.get('special', '')

    # Combine general and specialization-specific courses
    curriculum: list[str] = list(major_curriculum["general"])
    curriculum.extend(major_curriculum.get(specialization, []))

    remaining_courses = set()
    def check_and_add_course(course: str):
        if course in taken_courses:
            return  # already completed

        # If course has prereq information
        course_reqs = prereq_info.get(course, {})
        all_requirements = course_reqs.get('pre-req', []) + course_reqs.get('concur', [])

        for prereq_group in all_requirements:
            # At least one course from the group must be satisfied
            if not any(c in taken_courses for c in prereq_group):
                # None satisfied, recursively add the first unsatisfied prereq course
                prereq_course = prereq_group[0]
                check_and_add_course(prereq_course)

        # After checking prerequisites, finally add this course itself
        remaining_courses.add(course)

    # Check each curriculum course
    for course in curriculum:
        check_and_add_course(course)

    # Filter out courses that are already taken
    return sorted(remaining_courses - taken_courses)