from models import *
from genetic import genetic

math = Subject("math")
physics = Subject("physics")
geography = Subject("geography")
chemistry = Subject("chemistry")
history = Subject("history")
a1 = Audience("a1")
a2 = Audience("a2")
a3 = Audience("a3")
a4 = Audience("a4")
g1 = Group("g1", [(physics,2), (chemistry,3)])
g2 = Group("g2", [(math,2), (physics,3)])
g3 = Group("g3", [(geography,4)])
g4 = Group("g4", [(physics,3), (geography,1)])
g5 = Group("g5", [(geography,1), (history,4)])
bob = Teacher("Bob", 20, [physics, chemistry])
mike = Teacher("Mike", 10, [math, physics])
milton = Teacher("Milton", 25, [geography])
dave = Teacher("Dave", 15, [chemistry])
yoko = Teacher("Yoko", 25, [history])
teachers = [bob, mike, milton, dave, yoko]
audiences = [a1, a2, a3, a4]
groups = [g1, g2, g3, g4, g5]
subjects = [math, physics, geography, chemistry, history]
max_lessons = 3

g = genetic(subjects,teachers,groups,audiences,max_lessons)
schedule = g.solve(500, 1000, 0.8, 0.001)
for p in schedule[0]:
    p.print()
    print("--------")
print(f"fitness: {schedule[1]}")