import json
import pathlib
from canvasapi import Canvas

config_path = str(pathlib.Path(__file__).parents[1])
with open(f'{config_path}/api_config.json') as f:
    config = json.load(f)

class Course_and_Quizzes:
    def __init__(self):
        self.api_url = config['api_url']
        self.api_key = config['access_token']

        # Initialize a new Canvas object and get all the courses
        canvas = Canvas(self.api_url, self.api_key)

        print("Choose a course from the list of Courses:")
        courses,i = [],1
        for item in canvas.get_courses():
            courses.append(item)
            print(f'{i}. {item}')
            i+=1

        print("")
        course_index = input("Enter the Course index (Eg input: 1): ")
        # course_index = '1'

        self.course = canvas.get_course(courses[int(course_index)-1])

        # Get all quizes in the course
        quizzes = [item for item in self.course.get_quizzes()]
        print("Choose all the quizzes from the list of quizzes:")
        for i in range(len(quizzes)):
            print(f'{i+1}. {quizzes[i]}') 

        quiz_indices = input("Enter the quiz indicies (Eg input: 1 2 3): ")
        # quiz_indices = '1 3 5'

        quiz_indices = quiz_indices.strip().split(" ")

        self.quizzes = [quizzes[int(item)-1] for item in quiz_indices]

