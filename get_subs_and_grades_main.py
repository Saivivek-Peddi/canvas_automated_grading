from get_course_and_quizzes import Course_and_Quizzes
from get_submissions import Submissions
from get_groups import Groups
from get_grades import Grade
from clean import Clean

Clean()
cq = Course_and_Quizzes()
submissions = Submissions(cq.quizzes)
groups = Groups(cq.course)
Grade(cq.quizzes)

# print(cq.course)
# print(cq.quizzes)

# quizz = cq.quizzes[2]
# quizz_report = quizz.create_report('student_analysis')
