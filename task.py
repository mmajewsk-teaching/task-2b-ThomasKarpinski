import json
import random
from typing import Dict, List, Any, Optional
from functools import reduce

DATA_FILEPATH = 'school_data.json'
COURSES = ["Mathematics", "Physics", "History", "Polish", "Computer Science", "Biology"]
SCHOOL_NAMES = ["Highschool VI", "Highschool III"]

SchoolData = Dict[str, Dict[str, Any]]


def generate_initial_data(num_schools: int, num_students_per_school: int) -> SchoolData:
    data: SchoolData = {}
    
    names = ["Adam", "Bartosz", "Anna", "Ewa", "Katarzyna", "Michał", "Piotr", "Wiktoria", "Jakub", "Zofia"]
    surnames = ["Kowalski", "Nowak", "Wiśniewski", "Wójcik", "Kowalczyk", "Lewandowski", "Zieliński", "Szymański"]

    for i in range(num_schools):
        school_id = f"SCHOOL_{i+1:02d}"
        school_name = SCHOOL_NAMES[i % len(SCHOOL_NAMES)]
        
        data[school_id] = {"name": school_name, "students": {}}
        
        for j in range(num_students_per_school):
            student_id = f"{school_id}_S{j+1:02d}"
            
            student_scores = {}
            student_attendance = {}
            for course in COURSES:
                num_scores = random.randint(3, 6)
                scores = [random.choice([2.0, 3.0, 3.5, 4.0, 4.5, 5.0]) for _ in range(num_scores)]
                student_scores[course] = scores
                
                student_attendance[course] = random.randint(10, 20)

            data[school_id]["students"][student_id] = {
                "name": random.choice(names),
                "surname": random.choice(surnames),
                "enrollment_year": random.randint(2021, 2023),
                "scores": student_scores,
                "attendance": student_attendance,
            }
            
    return data


def load_data(filepath: str) -> Optional[SchoolData]:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            print(f"{filepath}")
            return json.load(f)
    except FileNotFoundError:
        print(f"File '{filepath}' doesn't exist. New data will be generated.")
        return None

def save_data(data: SchoolData, filepath: str) -> None:
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Data savet do filr: {filepath}")
    except IOError as e:
        print(f"Saving data error {e}")


def find_student_details(data: SchoolData, student_id: str) -> Optional[Dict[str, Any]]:
    for school_id in data:
        if student_id in data[school_id]["students"]:
            return data[school_id]["students"][student_id]
    return None


def calculate_student_class_average(data: SchoolData, student_id: str, course_name: str) -> Optional[float]:
    student_details = find_student_details(data, student_id)
    
    if not student_details or course_name not in student_details["scores"]:
        return None

    scores = student_details["scores"][course_name]
    
    if not scores:
        return 0.0
        
    average = sum(scores) / len(scores) 
    
    
    return round(average, 2)


def calculate_student_total_average(data: SchoolData, student_id: str) -> Optional[float]:
    student_details = find_student_details(data, student_id)
    if not student_details:
        return None

    all_scores = []
    
    for course in COURSES:
        if course in student_details["scores"]:
            all_scores.extend(student_details["scores"][course])

    if not all_scores:
        return 0.0

    total_average = sum(all_scores) / len(all_scores)
    return round(total_average, 2)


def get_student_attendance_summary(data: SchoolData, student_id: str) -> Optional[int]:
    student_details = find_student_details(data, student_id)
    if not student_details:
        return None
        
    total_attendance = reduce(
        lambda acc, course_attendance: acc + course_attendance, 
        student_details["attendance"].values(), 
        0
    )
    
    return total_attendance


def get_top_students_by_school_average(data: SchoolData, school_id: str, limit: int = 5) -> Optional[List[Dict[str, Any]]]:
    if school_id not in data:
        return None
        
    students_data = []
    
    for student_id, details in data[school_id]["students"].items():
        avg = calculate_student_total_average(data, student_id)
        if avg is not None:
            students_data.append({
                "id": student_id,
                "name": f"{details['name']} {details['surname']}",
                "average": avg
            })
            

    sorted_students = sorted(
        students_data, 
        key=lambda x: x["average"], 
        reverse=True
    )
    
    return sorted_students[:limit]


def get_course_high_achievers(data: SchoolData, course_name: str, min_average: float = 4.5) -> List[Dict[str, Any]]:
    high_achievers = []

    for school_id, school_details in data.items():
        for student_id, student_details in school_details["students"].items():
            avg = calculate_student_class_average(data, student_id, course_name)
            
            if avg is not None and avg >= min_average:
                high_achievers.append({
                    "school_name": school_details["name"],
                    "name": f"{student_details['name']} {student_details['surname']}",
                    "course_average": avg
                })
                
    return sorted(high_achievers, key=lambda x: x["name"])


def main() -> None:
    
    school_data = load_data(DATA_FILEPATH)
    if school_data is None:
        print("Generating data...")
        school_data = generate_initial_data(
            num_schools=len(SCHOOL_NAMES), 
            num_students_per_school=10
        )

    school_ids = list(school_data.keys())
    if not school_ids:
        print("No data")
        return
        
    school_a_id = school_ids[0]
    
    student_ids_a = list(school_data[school_a_id]["students"].keys())
    test_student_id = student_ids_a[0]
    test_course = COURSES[0]
    
    test_student_details = find_student_details(school_data, test_student_id)
    
    
    print(f"Information about student({test_student_id})")
    print(f"Name and Surname: {test_student_details['name']} {test_student_details['surname']}")
    print(f"School: {school_data[school_a_id]['name']}")

    class_avg = calculate_student_class_average(school_data, test_student_id, test_course)
    print(f"Average of {test_course}: {class_avg if class_avg is not None else 'No data'}")
    
    print(f"Grades in course {test_course}: {test_student_details['scores'][test_course]}")

    total_avg = calculate_student_total_average(school_data, test_student_id)
    print(f"Average of all courses: {total_avg if total_avg is not None else 'no data'}")

    attendance = get_student_attendance_summary(school_data, test_student_id)
    print(f"Attendence number: {attendance if attendance is not None else 'no data'}")

    print(f"\n Best Students from {SCHOOL_NAMES[0]}")
    top_students = get_top_students_by_school_average(school_data, school_a_id, limit=5)
    if top_students:
        for i, student in enumerate(top_students):
            print(f"{i+1}. {student['name']}: Average: {student['average']:.2f}")

    print("\nCourse: Physics - Students with high average (>= 4.75)")
    high_achievers = get_course_high_achievers(school_data, "Physics", min_average=4.75)
    if high_achievers:
        for student in high_achievers:
            print(f"- {student['name']} ({student['school_name']}): {student['course_average']:.2f}")
    else:
        print("No such students")
        

    save_data(school_data, DATA_FILEPATH)


if __name__ == "__main__":
    main()
