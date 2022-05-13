import sys

N = int(sys.stdin.readline().rstrip())

list_course = []
for _ in range(N):
    start, end = (int(el) for el in sys.stdin.readline().split())
    list_course.append((start, end))

sorted_list_course = sorted(list_course, key=lambda x:x[1])
n_courses = 0
start_limit = 0
for course in sorted_list_course:
    start, end = course
    if start >= start_limit:
        n_courses+=1
        start_limit = end

print(n_courses)