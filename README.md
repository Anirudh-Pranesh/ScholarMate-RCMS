# ScholarMate-RCMS

ScholarMate is an RCMS, being made for CS class 12 project by Anirudh, Dave & Vignesh

ScholarMate can be used by schools for handling their students' marks and keeping a secure and safe record of them. The sofwatre provides visual analytics of marks for each and every student who has written an exam, and also provides a comparison for the class averages. The program may be used to generate report cards for every student that has written an exam within seconds, and also includes many other features, described in the **How to use ScholarMate** section.

The file attatched below describes the design of the software, describing all the features and functionalities included in the software.

https://drive.google.com/file/d/1XUFr5fEAIPeqqcX7lUnfNcna0rNyRoBH/view?usp=sharing

![alt text](image.png)

The file attatched bellow describes the MySQL database structure

https://drive.google.com/file/d/1QQCceEJRKtQzwJt2dB5-S4vGCiToQtWy/view?usp=sharing

![alt text](image-1.png)

The software is open source and here is the list of all the required imports and downloads for the source code : 

# REQUIRED INSTALLS : 

-> pip install pillow (for inserting image)<br />
-> pip install sv_ttk (for the theme)<br />
-> pip install fpdf (pdf generation)<br />
-> pip install mysql.connector<br />
-> pip install matplotlib (Graph generation)

# How to use ScholarMate ? 

Open login_page.py and enter your username and password. 

As an admin you are allowed multiple access rights to the database server. You are allowed to create a new examination/a sheet for teachers to enter their student's marks, you are allowed to edit the schools directory by adding/removing teachers/students, you are allowed to generate report cards, view any student's/class' marks in a given exam and allowed to edit any student's marks in any exam. The user icon on the left hand side blue bar allows you to change your username and password. You can conveniently log out as well. 

As a teacher, you are assigned to be the class teacher of a given class. You are allowed a restricted access to the database server. First and foremost, you are only allowed to view/edit your own class' marks. You cannot see or edit any other class' marks. You can generate report cards, but only for the students in your class.

As a student, you can only view your marks and generate your own report card

Here are some usernames and passwords that you may use for testing purposes : 

**Username and Password of admin :** 

Username : _admin Password: _admin

**Username and Password of a few students : **

Aarti Bansal_94          Aarti Bansal_94
Reyansh Jain_7           Reyansh Jain_7
Vivaan Sharma_2        Vivaan Sharma_2
Ayaan Mehta_6           Ayaan Mehta_6
Kartik Agarwal_8         Kartik Agarwal_8

**Username and Password of all teachers :** 

Mr. Arjun Gupta_5         Mr. Arjun Gupta_5
Mr. Rajesh Kumar_7      Mr. Rajesh Kumar_7
Mr. Ramesh Patel_1      Mr. Ramesh Patel_1
Mr. Vikram Sharma_3   Mr. Vikram Sharma_3
Mrs. Sanya Desai_8     Mrs. Sanya Desai_8
Ms. Ananya Singh_2    Ms. Ananya Singh_2
Ms. Neha Verma_6      Ms. Neha Verma_6
Ms. Priya Rao_4          Ms. Priya Rao_4

For more student usernames, you may access the MySQL database. The host, username, and password are given in the source code. You may access either through your terminal or through MySQL workbench. To get more usernames and passwords, run this SQL statement to the server : 

```SQL
SELECT * FROM credentials;
```

# DISCLAIMER 

As of now, the **"Edit school directory"** feature is currently **UNAVAILABLE** due to server issues. This feature is only available for localhost release where the database server issues have been resolved. We apologise for any inconvenience caused.
