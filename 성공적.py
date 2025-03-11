#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys

def get_filename():
    filename = input("Enter filename (default 'students.txt'): ").strip()
    return filename if filename else "students.txt"

def calculate_average(midterm, final):
    return (float(midterm) + float(final)) / 2

def calculate_grade(avg):
    if avg >= 90:
        return 'A'
    elif avg >= 80:
        return 'B'
    elif avg >= 70:
        return 'C'
    elif avg >= 60:
        return 'D'
    else:
        return 'F'

def load_data(filename):
    """
    파일에서 데이터를 읽어 학생 정보를 딕셔너리로 저장합니다.
    각 줄은 학번, 이름, 중간고사, 기말고사 순으로 주어지며,
    탭('\t')이 있을 경우 탭을 기준으로, 없으면 공백을 기준으로 분리합니다.
    """
    students = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                # 탭으로 분리; 없으면 공백으로 분리
                if "\t" in line:
                    parts = line.split("\t")
                else:
                    parts = line.split()
                if len(parts) < 4:
                    continue
                student_id = parts[0]
                # 이름에 공백이 포함될 수 있으므로 1부터 -2까지 합침
                name = " ".join(parts[1:-2]) if len(parts) > 4 else parts[1]
                try:
                    mid = int(parts[-2])
                    final = int(parts[-1])
                except ValueError:
                    continue
                avg = calculate_average(mid, final)
                grade = calculate_grade(avg)
                students[student_id] = {
                    "id": student_id,
                    "name": name,
                    "mid": mid,
                    "final": final,
                    "average": avg,
                    "grade": grade
                }
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        sys.exit(1)
    return students

def save_data(students, filename):
    """
    학생 데이터를 평균 점수를 기준으로 내림차순 정렬하여 파일에 저장합니다.
    저장 형식: 학번, 이름, 중간고사, 기말고사 (각 항목은 탭으로 구분)
    """
    sorted_students = sorted(students.values(), key=lambda s: s["average"], reverse=True)
    with open(filename, 'w') as file:
        for s in sorted_students:
            file.write(f"{s['id']}\t{s['name']}\t{s['mid']}\t{s['final']}\n")

def show(students):
    """
    전체 학생 정보를 평균 점수를 기준으로 내림차순 정렬하여 출력합니다.
    출력 형식: 학번, 이름, 중간고사, 기말고사, 평균(소수점 첫째자리), 학점
    """
    sorted_students = sorted(students.values(), key=lambda s: s["average"], reverse=True)
    print("학번\t\t이름\t\t중간고사\t기말고사\t평균\t학점")
    print("--------------------------------------------------------------------")
    for s in sorted_students:
        print(f"{s['id']}\t{s['name']}\t{s['mid']}\t{s['final']}\t{s['average']:.1f}\t{s['grade']}")

def search(students, student_id):
    """
    입력받은 학번으로 학생 정보를 검색하여 출력합니다.
    존재하지 않으면 "NO SUCH PERSON." 메시지를 출력합니다.
    """
    if student_id in students:
        s = students[student_id]
        print("학번\t\t이름\t\t중간고사\t기말고사\t평균\t학점")
        print("--------------------------------------------------------------------")
        print(f"{s['id']}\t{s['name']}\t{s['mid']}\t{s['final']}\t{s['average']:.1f}\t{s['grade']}")
    else:
        print("NO SUCH PERSON.")

def changescore(students, student_id):
    """
    해당 학번 학생의 중간(mid) 또는 기말(final) 점수를 수정합니다.
    - 존재하지 않는 학번일 경우 "NO SUCH PERSON." 출력
    - exam type이 'mid' 또는 'final'이 아니면 무시
    - 입력 점수가 0~100 범위가 아니면 무시
    수정 후 평균과 학점도 재계산합니다.
    """
    if student_id not in students:
        print("NO SUCH PERSON.")
        return

    exam_type = input("Mid/Final? ").strip().lower()
    if exam_type not in ['mid', 'final']:
        return

    try:
        new_score = int(input("Input new score: ").strip())
        if 0 <= new_score <= 100:
            s = students[student_id]
            
            # 수정 전 정보 출력
            print("학번\t\t이름\t\t중간고사\t기말고사\t평균\t학점")
            print("--------------------------------------------------------------------")
            print(f"{s['id']}\t{s['name']}\t{s['mid']}\t{s['final']}\t{s['average']:.1f}\t{s['grade']}")
            
            # 해당 점수 수정
            if exam_type == 'mid':
                s['mid'] = new_score
            elif exam_type == 'final':
                s['final'] = new_score

            # 점수 수정 후 평균 및 학점 재계산
            mid = s["mid"]
            final = s["final"]
            avg = calculate_average(mid, final)
            s["average"] = avg
            s["grade"] = calculate_grade(avg)
            
            # 수정 후 정보 출력
            print(f"{s['id']}\t{s['name']}\t{s['mid']}\t{s['final']}\t{s['average']:.1f}\t{s['grade']}")
        else:
            return
    except ValueError:
        return


def add(students, student_id):
    # 이미 존재하는 학번이면 메시지 출력 후 종료
    if student_id in students:
        print("ALREADY EXISTS.")
        return

    # 학생의 이름, 중간, 기말 점수를 차례로 입력 받음
    name = input("Name: ").strip()
    midterm_input = input("Midterm Score: ").strip()
    final_input = input("Final Score: ").strip()

    try:
        mid = int(midterm_input)
        fin = int(final_input)
    except ValueError:
        print("Invalid score input.")
        return

    # 점수 범위(0~100) 검사
    if not (0 <= mid <= 100 and 0 <= fin <= 100):
        print("Invalid score input.")
        return

    avg = calculate_average(mid, fin)
    grade = calculate_grade(avg)
    students[student_id] = {
        "id": student_id,
        "name": name,
        "mid": mid,
        "final": fin,
        "average": avg,
        "grade": grade
    }
    print("Student added.")



def searchgrade(students, grade):
    """
    입력받은 학점(A, B, C, D, F)에 해당하는 학생들을 평균 내림차순으로 출력합니다.
    잘못된 학점이 입력되었거나 해당 학점의 학생이 없으면 적절한 메시지를 출력합니다.
    """
    valid_grades = ['A', 'B', 'C', 'D', 'F']
    if grade not in valid_grades:
        return
    filtered = [s for s in students.values() if s["grade"] == grade]
    if not filtered:
        print("NO RESULTS.")
        return
    filtered_sorted = sorted(filtered, key=lambda s: s["average"], reverse=True)
    print("학번\t\t이름\t\t중간고사\t기말고사\t평균\t학점")
    print("--------------------------------------------------------------------")
    for s in filtered_sorted:
        print(f"{s['id']}\t{s['name']}\t{s['mid']}\t{s['final']}\t{s['average']:.1f}\t{s['grade']}")

def remove(students, student_id):
    """
    학생 목록이 비어있으면 "List is empty."를 출력합니다.
    존재하지 않는 학번이면 "NO SUCH PERSON."를 출력하며,
    정상적으로 삭제되면 "Student removed." 메시지를 출력합니다.
    """
    if not students:
        print("List is empty.")
        return
    if student_id not in students:
        print("NO SUCH PERSON.")
        return
    del students[student_id]
    print("Student removed.")

def main():
    filename = get_filename()
    students = load_data(filename)
    while True:
        command = input("# ").strip().lower()
        if command == "show":
            show(students)
        elif command == "search":
            sid = input("Student ID: ").strip()
            search(students, sid)
        elif command == "changescore":
            sid = input("Student ID: ").strip()
            changescore(students, sid)
        elif command == "add":
            sid = input("Student ID: ").strip()
            add(students, sid)
        elif command == "searchgrade":
            grade = input("Grade to search: ").strip().upper()
            searchgrade(students, grade)
        elif command == "remove":
            sid = input("Student ID: ").strip()
            remove(students, sid)
        elif command == "quit":
            save_choice = input("Save data?[yes/no] ").strip().lower()
            if save_choice == "yes":
                new_file = input("File name: ").strip()
                save_data(students, new_file)
            break
        else:
            print("# ", end="")


if __name__ == "__main__":
    main()


# In[ ]:




