# ScholarMate 🏫
[![GPL License](https://badges.frapsoft.com/os/gpl/gpl.png?v=103)](https://opensource.org/licenses/GPL-3.0/)
[![python](https://img.shields.io/badge/Python-3.11.4-3776AB.svg?style=flat&logo=python&logoColor=yellow)](https://www.python.org)
[![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=flat&logo=mysql&logoColor=black)](https://img.shields.io/badge/MySQL-4479A1.svg?style=for-the-badge&logo=MySQL&logoColor=white)

```

           $$$$$$\            $$\                 $$\                           $$\      $$\            $$\               
          $$  __$$\           $$ |                $$ |                          $$$\    $$$ |           $$ |              
          $$ /  \__| $$$$$$$\ $$$$$$$\   $$$$$$\  $$ | $$$$$$\   $$$$$$\        $$$$\  $$$$ | $$$$$$\ $$$$$$\    $$$$$$\  
          \$$$$$$\  $$  _____|$$  __$$\ $$  __$$\ $$ | \____$$\ $$  __$$\       $$\$$\$$ $$ | \____$$\\_$$  _|  $$  __$$\ 
           \____$$\ $$ /      $$ |  $$ |$$ /  $$ |$$ | $$$$$$$ |$$ |  \__|      $$ \$$$  $$ | $$$$$$$ | $$ |    $$$$$$$$ |
          $$\   $$ |$$ |      $$ |  $$ |$$ |  $$ |$$ |$$  __$$ |$$ |            $$ |\$  /$$ |$$  __$$ | $$ |$$\ $$   ____|
          \$$$$$$  |\$$$$$$$\ $$ |  $$ |\$$$$$$  |$$ |\$$$$$$$ |$$ |            $$ | \_/ $$ |\$$$$$$$ | \$$$$  |\$$$$$$$\ 
           \______/  \_______|\__|  \__| \______/ \__| \_______|\__|            \__|     \__| \_______|  \____/  \_______|
                                                                                                                
```                                                                                                                
                                                                                                                
ScholarMate is an RCMS (Report Card Managament System), under development for CS class 12 project by Anirudh, Dave & Vignesh

ScholarMate can be used by schools for handling their students' marks and keeping a secure and safe record of them. The sofwatre provides visual analytics of marks for each and every student who has written an exam, and also provides a comparison for the class averages. The program may be used to generate report cards for every student that has written an exam within seconds, and also includes many other features, described in the **How to use ScholarMate** section.

The file attatched below describes the design of the software, describing all the features and functionalities included in the software.

https://drive.google.com/file/d/1XUFr5fEAIPeqqcX7lUnfNcna0rNyRoBH/view?usp=sharing

The file attatched bellow describes the MySQL database structure

https://drive.google.com/file/d/1QQCceEJRKtQzwJt2dB5-S4vGCiToQtWy/view?usp=sharing



# Screenshots : 

![alt text](image.png)

![alt text](image-1.png)

![image](https://github.com/user-attachments/assets/011f5dc0-c9dd-4524-a1c0-be1dc299254d)

![image](https://github.com/user-attachments/assets/4aa0783d-2d18-4b91-8886-53a07eb0263a)

**Sample report card :**

[REPORTCARD_Semester1_Aarti Sharma_50.pdf](https://github.com/user-attachments/files/17462897/REPORTCARD_Semester1_Aarti.Sharma_50.pdf)

# Installation 🖥️

First, install python, after which run the following commands on your terminal

Use the first command on windows, and the second if you're on mac

➡️ pip install pillow or pip3 install pillow (for inserting image)<br />
➡️ pip install sv_ttk or pip3 install sv_ttk (for the theme)<br />
➡️ pip install fpdf or pip3 install fpdf (pdf generation)<br />
➡️ pip install mysql.connector or pip3 install mysql.connector (for MySQL connection)<br />
➡️ pip install matplotlib or pip3 install matplotlib (Graph generation)

Download the zip file of this project and run ```login_page.py```

# How to use ScholarMate ? 👤

Open login_page.py and enter your username and password. 

As an admin you are allowed multiple access rights to the database server. You are allowed to create a new examination/a sheet for teachers to enter their student's marks, you are allowed to edit the schools directory by adding/removing teachers/students, you are allowed to generate report cards, view any student's/class' marks in a given exam and allowed to edit any student's marks in any exam. The user icon on the left hand side blue bar allows you to change your username and password. You can conveniently log out as well. 

As a teacher, you are assigned to be the class teacher of a given class. You are allowed a restricted access to the database server. First and foremost, you are only allowed to view/edit your own class' marks. You cannot see or edit any other class' marks. You can generate report cards, but only for the students in your class.

As a student, you can only view your marks and generate your own report card

Here are some usernames and passwords that you may use for testing purposes : 

**Username and Password of admin :** 

➡️Username : _admin Password: _admin

**Username and Password of a few students :**

➡️Aarti Bansal_94<br />
➡️Reyansh Jain_7<br />
➡️Vivaan Sharma_2<br />
➡️Ayaan Mehta_6<br />
➡️Kartik Agarwal_8<br />

**Username and Password of all teachers :** 

➡️Mr. Arjun Gupta_5<br />
➡️Mr. Rajesh Kumar_7<br />
➡️Mr. Ramesh Patel_1<br />
➡️Mr. Vikram Sharma_3<br />
➡️Mrs. Sanya Desai_8<br />
➡️Ms. Ananya Singh_2<br />
➡️Ms. Neha Verma_6<br />
➡️Ms. Priya Rao_4<br />

For more student usernames, you may access the MySQL database. The host, username, and password are given in the source code. You may access either through your terminal or through MySQL workbench. To get more usernames and passwords, run this SQL statement to the server: 

```SQL
SELECT * FROM credentials;
```

# DISCLAIMER ⚠️

As of now, the **"Edit school directory"** feature is currently **UNAVAILABLE** due to server issues. This feature is only available for localhost release where the database server issues have been resolved. We apologise for any inconvenience caused.

# Documentation 📃

Coming soon ...
