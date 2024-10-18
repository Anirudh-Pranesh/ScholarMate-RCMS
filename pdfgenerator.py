import os
from fpdf import FPDF
import matplotlib.pyplot as plt
from tkinter import messagebox
import os
from pathlib import Path

#get downloads folder
home = str(Path.home())
downloads_folder = os.path.join(home, "Downloads")


class PDF(FPDF):
    def header(self):
        # School Name
        self.set_text_color(39, 75, 176)
        self.set_font("Arial", "B", 14,)
        self.cell(0, 10, "Bharat School", 0, 1, "C")
        self.set_text_color(0, 0, 0)
        self.ln(10)

    def chapter_title(self, title):
        self.set_text_color(0, 128, 255)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1, "L")
        self.set_text_color(0, 0, 0)
        self.ln(5)

    def chapter_body(self, body):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, body)
        self.ln()

def get_grade(score):
    """Returns the grade based on the score."""
    if 91 <= score <= 100:
        return 'A1'
    elif 81 <= score <= 90:
        return 'A2'
    elif 71 <= score <= 80:
        return 'B1'
    elif 61 <= score <= 70:
        return 'B2'
    elif 51 <= score <= 60:
        return 'C1'
    elif 41 <= score <= 50:
        return 'C2'
    elif 33 <= score <= 40:
        return 'D'
    elif score <= 32:
        return 'F'

def create_bar_graph(subjects, student_scores, top_scores, average_scores):
    """Creates a bar graph comparing student scores, top scores, and average scores."""
    bar_width = 0.2
    
    r1 = range(len(subjects))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width * 2 for x in r1]

    plt.figure(figsize=(10, 6))

    plt.bar(r1, student_scores, color='blue', width=bar_width, label='Student Score')
    plt.bar(r2, top_scores, color='red', width=bar_width, label='Top Score')
    plt.bar(r3, average_scores, color='green', width=bar_width, label='Grade Avg Score')

    for i in range(len(subjects)):
        plt.text(r1[i], float(student_scores[i]) + 0.5, str(student_scores[i]), ha='center')
        plt.text(r2[i], float(top_scores[i]) + 0.5, str(top_scores[i]), ha='center')
        plt.text(r3[i], float(average_scores[i]) + 0.5, str(average_scores[i]), ha='center')

    plt.xlabel('Subjects')
    plt.ylabel('Scores')
    plt.title('Student vs Top vs Grade Avg Scores')
    plt.xticks([r + bar_width for r in range(len(subjects))], subjects)
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Save the graph as an image
    plt.savefig("bar_graph.png")
    plt.close()

def generate_report_card(student_name, teacher_name, parent_contact, teacher_contact,
                         class_name, exam_name, scores, top_scores, average_scores, student_id, subjects):
    pdf = PDF()
    pdf.add_page()

    # First Page Content
    pdf.chapter_title(f"Report for {exam_name}")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Student Name: {student_name}", 0, 1)
    pdf.cell(0, 10, f"Teacher Name: {teacher_name}", 0, 1)
    pdf.cell(0, 10, f"Parent Contact: {parent_contact}", 0, 1)
    pdf.cell(0, 10, f"Teacher Contact: {teacher_contact}", 0, 1)
    pdf.cell(0, 10, f"Class: {class_name}", 0, 1)
    pdf.cell(0, 10, "", 0, 1)  # Blank line
    pdf.cell(0, 10, f"Exam Name: {exam_name}", 0, 1)
    pdf.ln(10)

    # Second Page: Marksheet
    pdf.add_page()
    pdf.chapter_title("Marksheet")

    # Table Header
    pdf.set_font("Arial", "B", 12)
    pdf.cell(50, 10, "Subject", 1)
    pdf.cell(40, 10, "Student Score", 1)
    pdf.cell(40, 10, "Top Score", 1)
    pdf.cell(40, 10, "Grade Avg Score", 1)
    pdf.cell(40, 10, "Grade", 1)
    pdf.ln()

    # Table Rows
    pdf.set_font("Arial", "", 12)
    total_score = 0

    for i, subject in enumerate(subjects):
        student_score = scores[i]
        total_score += student_score
        grade = get_grade(student_score)

        pdf.cell(50, 10, subject, 1)
        pdf.cell(40, 10, str(student_score), 1)
        pdf.cell(40, 10, str(top_scores[i]), 1)
        pdf.cell(40, 10, str(average_scores[i]), 1)
        pdf.cell(40, 10, grade, 1)
        pdf.ln()

    # Total and Average
    average_student_score = total_score / len(subjects)
    pdf.cell(50, 10, "Total Score", 1)
    pdf.cell(40, 10, str(total_score), 1, 0)
    pdf.cell(40, 10, "", 1)
    pdf.cell(40, 10, "", 1)
    pdf.cell(40, 10, "", 1)
    pdf.ln()

    pdf.cell(50, 10, "Your total Average Score", 1)
    pdf.cell(40, 10, str(average_student_score), 1, 0)
    pdf.cell(40, 10, "", 1)
    pdf.cell(40, 10, "", 1)
    pdf.cell(40, 10, "", 1)

    # Embed Bar Graph
    create_bar_graph(subjects, scores, top_scores, average_scores)
    pdf.add_page()
    pdf.chapter_title("Performance Analysis")
    pdf.image("bar_graph.png", x=10, y=50, w=180)  # Embed the saved bar graph image

    # Save PDF
    file_path = f"REPORTCARD_{exam_name}_{student_name}_{student_id}.pdf"
    pdf_path = os.path.join(downloads_folder, file_path)
    #file_path = f"/Users/adminREPORTCARD_{exam_name}_{student_name}_{student_id}.pdf"
    pdf.output(pdf_path)
    os.remove('bar_graph.png')
