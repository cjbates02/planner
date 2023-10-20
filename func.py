class User:
    def __init__(self, name, year, courses):
        self.name = name # string (student name)
        self.year = year # integer (sophomore, junior, etc.)
        self.courses = courses # list
    
    # this functions maps each day of the week with all corresponding courses on that day
    def create_schedule(self):
        schedule = {'Monday' : [], 'Tuesday' : [], 'Wednesday' : [], 'Thursday' : [], 'Friday' : []}

        for c in self.courses:
            for d in c.meeting_days:
                schedule[d].append(c)

        return schedule

    # this function creates a view of the student schedule
    # schedule - dictionary
    def view_schedule(self, _schedule):
        for key in _schedule:
            if _schedule[key]:
                for course in _schedule[key]:
                    print(key)
                    print(course.title)
                    print(course.meeting_time)

                          

class Course:

    def __init__(self, title, instructor, meeting_time, grade, meeting_days):
        self.title = title # string
        self.instructor = instructor # string
        self.meeting_days = meeting_days # ['Monday', ... , 'Friday']
        self.meeting_time = meeting_time #  [[starting time1, ending time1], ...]
        self.grade = grade # float (number grade)
    

        
        
    

