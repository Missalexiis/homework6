class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def leave_feedback(self, lecturer, course, grade):
        if isinstance(lecturer,
                      Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.student_feedback:
                lecturer.student_feedback[course] += [grade]
            else:
                lecturer.student_feedback[course] = [grade]
        else:
            return 'Ошибка'

    def _average_rating(self, grade):
        average_rating = []
        courses = []
        for key, value in self.grades.items():
            average_rating += value
            if key not in courses:
                courses.append(key)
            else:
                courses += key
        mean = round((sum(average_rating) / len(average_rating)), 1)
        if grade == 'grade':
            return mean
        elif grade == 'list courses':
            return courses

    def __str__(self):
        grade = 'grade'
        list_courses_with_grade = 'list courses'
        res = (f"\nИмя: {self.name}"
               f"\nФамилия: {self.surname}"
               f"\nСредняя оценка за домашние задания: {self._average_rating(grade)}"
               f"\nКурсы в процессе изучения: {', '.join(self._average_rating(list_courses_with_grade))}"
               f"\nЗавершенные курсы: {', '.join(self.finished_courses)}")
        return res

    def __lt__(self, other):
        grade = 'grade'
        if not isinstance(other, Lecturer):
            print('Not a Lecturer')
            return
        return self._average_rating(grade) < other.average_feedback()

    def __gt__(self, other):
        grade = 'grade'
        if not isinstance(other, Lecturer):
            print('Not a Lecturer')
            return
        return self._average_rating(grade) > other.average_feedback()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.student_feedback = {}

    def average_feedback(self):
        average_feedback_list = []
        for key, value in self.student_feedback.items():
            average_feedback_list += value
        mean = round((sum(average_feedback_list) / len(average_feedback_list)), 1)
        return mean

    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.average_feedback()}'
        return res


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}'
        return res


def average_rating_students(course, *students):
    """
    Функция по подсчету средней оценки всех студентов в рамках конкретного курса"""
    list_st = []
    for student in students:
        if student.grades.get(course):
            list_st.extend(student.grades[course])
    return round(sum(list_st) / len(list_st), 1)


def average_feedback_lecturers(course, *lecturers):
    """
    Функция по подсчету средней оценки всех лекторов в рамках конкретного курса"""
    list_st = []
    for lecturer in lecturers:
        if lecturer.student_feedback.get(course):
            list_st.extend(lecturer.student_feedback[course])
    return round(sum(list_st) / len(list_st), 1)


# Создаем студентов
best_student_1 = Student('Name_student_1', 'Surname_student_1', 'your_gender')
best_student_2 = Student('Name_student_2', 'Surname_student_2', 'your_gender')

# Привязываем студентов к определенным курсам
best_student_1.courses_in_progress += ['Python']
best_student_2.courses_in_progress += ['Python']
best_student_1.courses_in_progress += ['GIT']
best_student_2.courses_in_progress += ['GIT']

best_student_1.finished_courses += ['Введение в программирование']
best_student_2.finished_courses += ['Введение в программирование']

# Создаем экспертов
reviewer_homeworks_1 = Reviewer("Name_reviewer_1", "Surname_reviewer_1")
reviewer_homeworks_2 = Reviewer("Name_reviewer_2", "Surname_reviewer_2")

# Привязываем экспертов к определенным курсам
reviewer_homeworks_1.courses_attached += ['Python']
reviewer_homeworks_1.courses_attached += ['GIT']
reviewer_homeworks_2.courses_attached += ['Python']
reviewer_homeworks_2.courses_attached += ['GIT']

# Эксперты проставляют оценки студентам
reviewer_homeworks_1.rate_hw(best_student_1, 'Python', 10)
reviewer_homeworks_1.rate_hw(best_student_1, 'Python', 8)
reviewer_homeworks_2.rate_hw(best_student_2, 'Python', 10)
reviewer_homeworks_2.rate_hw(best_student_2, 'Python', 7)
reviewer_homeworks_1.rate_hw(best_student_1, 'GIT', 10)
reviewer_homeworks_1.rate_hw(best_student_1, 'GIT', 6)
reviewer_homeworks_2.rate_hw(best_student_2, 'GIT', 10)
reviewer_homeworks_2.rate_hw(best_student_2, 'GIT', 9)

# Создаем лекторов
lector_course_1 = Lecturer('Name_lecturer_1', 'Surname_lecturer_1')
lector_course_2 = Lecturer('Name_lecturer_2', 'Surname_lecturer_2')

# Прикрепляем лекторов к курсам
lector_course_1.courses_attached += ['Python']
lector_course_1.courses_attached += ['GIT']
lector_course_2.courses_attached += ['Python']
lector_course_2.courses_attached += ['GIT']

# Cтуденты выставлют оценки
best_student_1.leave_feedback(lector_course_1, "Python", 10)
best_student_1.leave_feedback(lector_course_1, "Python", 9)
best_student_1.leave_feedback(lector_course_1, "GIT", 8)
best_student_1.leave_feedback(lector_course_1, "GIT", 7)
best_student_2.leave_feedback(lector_course_2, "Python", 10)
best_student_1.leave_feedback(lector_course_2, "Python", 9)
best_student_1.leave_feedback(lector_course_2, "GIT", 8)
best_student_1.leave_feedback(lector_course_2, "GIT", 7)  #

print(f"{'=' * 80}\n'Задание № 2. Атрибуты и взаимодействие классов.'")
print(f"\n{best_student_1.grades}")
print(f"\n{lector_course_1.student_feedback}")
print(f"\n{'=' * 80}\n'Задание № 3. Полиморфизм и магические методы'")
print(f"\n{reviewer_homeworks_1}")
print(f"\n{lector_course_1}")
print(f"\n{best_student_1}")

print(best_student_1 < lector_course_1)
print(best_student_1 > lector_course_1)

print(f"\n{'=' * 80}\n'Задание № 4. Полевые испытания'")
course = "GIT"
print(average_rating_students(course, best_student_1, best_student_2))
print(average_feedback_lecturers(course, lector_course_1, lector_course_2))
