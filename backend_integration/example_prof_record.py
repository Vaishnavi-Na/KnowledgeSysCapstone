import requests

from RMP_stuff import get_reviews, graphql_url, headers, data

'''
Stores an example RMP professor record.
If want to see more, run display_professor() (WARN: Could jam your console.)
'''

example_prof = {
    'avgDifficulty': 4.9, 'avgRating': 1.3, 'department': 'English', 'firstName': 'Irma', 'lastName': 'Zamora', 'legacyId': 2883698, 'numRatings': 7, 
    'Ratings': [
        {'index': 0, 'rating': None, 'comment': "Never left a review for a professor before, if that tells you how bad it is. You will never know what she is asking, how to navigate the modules, or what the grading criteria is. You have two peer reviews per assignment because she doesn't want to grade herself. Drop this class, it is not worth it. Most of your assignments aren't even for a grade."}, 
        {'index': 1, 'rating': None, 'comment': "I'm not one to write a bad review about a teacher but honestly if you get her for this class drop before you take it. I should've listened to people on this RMP this is honestly the most disorganized class I've ever taken. Grades are awful and other online sections are 10x better and 10x easier. So much work for an online class. DONT TAKE!"}, 
        {'index': 2, 'rating': None, 'comment': 'awful. just awful. very unclear instructions and very harsh grader. offers way too many assignments with unclear goals.'}, {'index': 3, 'rating': None, 'comment': 'Very disorganized modules, unclear instructions, and very nit-picky grading.'}, 
        {'index': 4, 'rating': None, 'comment': 'Extremely disorganized modules and way too many homework assignments for an online class.'}, 
        {'index': 5, 'rating': None, 'comment': 'Very tough grader throughout the course, required many assignments that were not graded. Gives lots of extra credit and bumps heavily by end of the semester. Very responsive in emails.'}, 
        {'index': 6, 'rating': None, 'comment': "She grades very tough and for a class that's all about readability, you can't understand what her assignments are asking. She had to postpone an assignment because she couldn't explain it. Be prepared to receive poor grades for no reason, and do many assignments that don't get graded at all. Don't take this class"}
    ]
}

def display_professor():
    for _ in range(2):
        #get html from graphql_url using set headers
        response = requests.post(graphql_url, headers=headers, json=data).json()
        # print(f"response: {response}")
        
        #for each professor, get their reviews and add elasticsearch index
        for professor in response["data"]["search"]["teachers"]["edges"]:            
            if professor["node"]["numRatings"]==0:
                return 

            get_reviews(professor["node"]["legacyId"],professor["node"])
            # es.index(index='professors', id=professor['node']['legacyId'], document=professor["node"])

            # print(professor["node"]["legacyId"])
            print(professor["node"])


        #pagination logic
        page_info = response["data"]["search"]["teachers"]["pageInfo"]
        if not page_info["hasNextPage"]:
            break  # Stop if no more pages

        #update cursor for next request
        data["variables"]["cursor"] = page_info["endCursor"]
    return

# display_professor()