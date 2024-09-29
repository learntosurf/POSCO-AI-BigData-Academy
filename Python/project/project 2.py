import sys

# 학생 클래스 정의
class Student:
    def __init__(self, student_number, name, midterm, final):
        self.student_number = student_number
        self.name = name
        self.midterm = midterm
        self.final = final
        self.average = (midterm + final) / 2 
        self.grade = self.assign_grade() 

    def assign_grade(self):
        if self.average >= 90:
            return 'A'
        elif self.average >= 80:
            return 'B'
        elif self.average >= 70:
            return 'C'
        elif self.average >= 60:
            return 'D'
        else:
            return 'F'
    
    def __repr__(self):
        return f"{self.student_number:<10} {self.name:<15} {self.midterm:<10} {self.final:<10} {self.average:<10.1f} {self.grade:<10}"

# 학생 정보 관리 클래스 정의
class StudentManager:
    def __init__(self, file_path="students.txt"):
        self.file_path = file_path
        self.students = self.read_student_data()

    # 파일 입출력 함수 
    def read_student_data(self):
        with open(self.file_path, "r") as file:
            students = []
            for line in file:
                # .strip(): 문자열의 앞과 뒤에 있는 공백을 제거
                # .split('\t'): 문자열을 탭 기준으로 나누어 리스트로 반환
                student_number, name, midterm, final = line.strip().split('\t') 
                # 학생 정보를 읽어 Student 객체 생성 후 리스트에 추가
                students.append(Student(student_number, name, int(midterm), int(final)))
            # print(students)
        return students

    def save_student_data(self, file_name=None):
        if file_name is not None:
            self.file_path = file_name
        sorted_students = sorted(self.students, key=lambda x: x.average, reverse=True)
        with open(self.file_path, "w") as file:
            for student in sorted_students:
                file.write(f"{student.student_number}\t{student.name}\t{student.midterm}\t{student.final}\n")

    def print_student_header(self):
        print(f"{'ID':<10} {'Student':<15} {'Midterm':<10} {'Final':<10} {'Average':<10} {'Grade':<10}")
        print("-" * 70)



    # 기능 구현
    # 1. show: 전체 학생 정보 출력 
    def show_students(self):
        sorted_students = sorted(self.students, key=lambda x: x.average, reverse=True)
        self.print_student_header()
        for student in sorted_students:
            print(student)


    # 2. search: 특정 학생 검색 
    def search_student(self):
        student_number = input("Student ID: ").strip()
        for student in self.students:
            if student.student_number == student_number:
                self.print_student_header()
                print(student)
                return
        print("NO SUCH PERSON.")


    # 3. changescore: 점수 수정 
    def change_student_score(self):
        student_number = input("Student ID: ").strip()
        # next(): 리스트에서 조건을 만족하는 첫 번째 요소 반환
        student = next((student for student in self.students if student.student_number == student_number), None)
        
        if student is None:
            print("NO SUCH PERSON.")
            return
        
        test_type = input("Mid/Final? ").strip().lower()
        if test_type not in ["mid", "final"]:
            return
        
        score = int(input("Input new score: "))
        if score < 0 or score > 100:
            return
        
        self.print_student_header()
        print(student)

        if test_type == "mid":
            student.midterm = score
        elif test_type == "final":
            student.final = score
        
        student.average = (student.midterm + student.final) / 2
        student.grade = student.assign_grade()

        self.save_student_data()
        
        print("Score changed.")
        print(student)


    # 4. add: 학생 추가 
    def add_student(self):
        student_number = input("Student ID: ").strip()
        student = next((student for student in self.students if student.student_number == student_number), None)
        
        if student is not None:
            print("ALREADY EXISTS.")
            return

        name = input("Name: ").strip()
        midterm = int(input("Midterm Score: "))
        final = int(input("Final Score: "))

        self.students.append(Student(student_number, name, midterm, final))
        self.save_student_data()
        print("Student added.")

    
    # 5. searchgrade: 학점 검색 
    def search_grade(self):
        grade = input("Grade to search: ").strip().upper()

        if grade not in ["A", "B", "C", "D", "F"]:
            return 

        matching_students = [student for student in self.students if student.grade == grade]

        if not matching_students:
            print("NO RESULTS.")
            return
        
        self.print_student_header()
        for student in matching_students:
            print(student)   


    # 6. remove: 특정 학생 삭제
    def remove_student(self):
        student_number = input("Student ID: ").strip()
        student = next((student for student in self.students if student.student_number == student_number), None)

        if not self.students:
            print("List is empty.")
            return
        
        if student is None:
            print("NO SUCH PERSON.")
            return
        
        self.students.remove(student)
        self.save_student_data()
        print("Student removed.")

    
    # 7. quit: 종료
    def quit_program(self):
        save = input("Save data? [yes/no]: ").strip().lower()
        if save == "yes":
            new_file_name = input("File name: ").strip()
            self.save_student_data(file_name=new_file_name)
        return False

    # 명령어 처리 함수
    def process_command(self, command):
        cmd = command.lower()
        
        if cmd == "show":
            self.show_students()
        elif cmd == "search":
            self.search_student()
        elif cmd == "changescore":
            self.change_student_score()
        elif cmd == "add":
            self.add_student()
        elif cmd == "searchgrade":
            self.search_grade()
        elif cmd == "remove":
            self.remove_student()
        elif cmd == "quit":
            return self.quit_program()
        else:
            # 잘못된 명령어 입력 시 에러 메세지 출력 없이 다시 명령어 입력 대기
            return True
        return True

# 프로그램 실행 함수
def main():
    # 파일 경로 입력 시 해당 파일을 읽어 학생 정보를 가져옴
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "students.txt"

    manager = StudentManager(file_path)
    # 프로그램 실행 시 학생들의 성적 목록 출력 
    manager.show_students()

    # 명령어 입력을 대기 
    while True:
        print()
        command = input("# ").strip()
        if not manager.process_command(command):
            break
        


if __name__ == "__main__":
    main()
