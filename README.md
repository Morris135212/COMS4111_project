# COMS4111_project
<center><i>Team member: Chenhui Mao (cm4054), Zihao Huang (zh2481)</i></center>

## Abstract
Database project. Build a web app to manage dataset and contest

## Commands to enter the database:
psql -U zh2481 -h 35.196.73.133 -d proj1part2

## URL of the project
35.243.164.83:8111

## Project proposal
The proposed application in this project is a platform for release and communication of datasets, it collects comprehensive information of various datasets for contest and project. The main page presents a list of datasets, users, competitions and courses. And the detailed information of datasets would be shown if the title is clicked. The specific contents include the brief introduction, provenance, solved and unsolved tasks from this dataset, discussions from users if applicable. For users, all of them are able to solve the problems from dataset and submit codes. Users in this application can participate in contests competitions and their scores and medals, which can later be used to present the rank of a competition, will be recorded and shown on the website. Moreover, users can contribute new datasets that are collected in their own researches, who ever contribute the datasets will be reseponsible for later maintainence. Meanwhile, some users may work for educational institutions, where datasets are used as teaching materials in courses. As mentioned, there are 7 entity sets in this scenerio, namely, users, datasets, tasks, codes, competitions, courses and universities. In project part 3 we will build our application with data come from Kaggle.

## Implemented functions
	1. The main page presents a list of datasets, users, competitions and courses.
	2. The detialed information of datasets can be accessed, including introduction provenance and tasks it stems.
	3. Users can participate in competitions, and there is a rank of score for each competition.
	4. All the user information can be accessed in the user list, including their scores, medals.
	5. Users can contribute new datasets.
    6. Users can submit code to the specific task
    7. Codes are ranked for the specific task by the stars they received.

## New features not mentioned
	1. New users are able to register.
	2. Current users can matintain dataset.
	3. Each user's followers can be viewed from user list page.
    4. User can sign up for the competition.

## Examples
	1. You can find all the users and their followers in the user list. And you can also register in the bottom part of this list, so you can see yourself in our page.

	2. You can roll down in the dataset page and visit the detial of the dataset called "Students Performance in Exams" to view its tasks.

	3. You can roll down to contribute a dataset in the dataset page with a registered user ID.

	4. You can update the dataset that you just contributed. (You cannot update others because only contributor of a dataset have permission to update it.)

	4. You can roll down in the dataset page and use the contribute function to contribute a custom named dataset to this database.

	5. You can sign in a listed competion.




