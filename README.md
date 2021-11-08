# COMS4111_project
<center><i>Team member: Chenhui Mao (cm4054), Zihao Huang (zh2481)</i></center>

## Abstract
Database project. Build a web app to manage dataset and contest

## Commands to enter the database:
psql -U zh2481 -h 35.196.73.133 -d proj1part2

## URL of the project
34.138.199.147:8111

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
	
	4. You can update the dataset if you are its contributor, for example, you can try to update the dataset <Trump's Dataset> as a user Donald Trump (You cannot update the one you just contributed TODAY because MAINTAIN records the date in days only and that would cause duplicate.)
	
	5. You can roll down in the dataset page and use the contribute function to contribute a custom named dataset to this database.
	
	6. You can sign in a listed competition.

### Scenario 1: Competition

When user enters into the main page, they will see a welcome sign, and below that, they will see the following existing competitions, user can see the detail of each competition by clicking <b>More</b>.

![main pages](https://raw.githubusercontent.com/Morris135212/COMS4111_project/main/app/static/images/competition.png)

In the next pages we can see that user can check the details of the competition including the start date, the end date, the prize and the number of participants. These details are actually queried from the database **given the name of the competition**. Also we can see that within the same page, we can check the Top-10 score from this competition, this is one of the interesting queries we submit for *project 1 part2*.

User can also choose to sign in for the competition by providing information including first name, last name, personal web pages, and university. Of course, the user must exist in the database, otherwise we will throw an error and direct to a fail page indicating that the user doesn't exist in the database.

![detail_competition](https://raw.githubusercontent.com/Morris135212/COMS4111_project/main/app/static/images/detail_competition.png)

### Scenario 2: Users

By clicking on the user button in the main page, we can enter into the User page, where we can see some details of all users in our system.  Here we can see that information includes users' name, the medal they obtained. Aslo by clicking on the users' image, we can enter into the personal page user provided in database. All this information are Selected from the database.

![User](https://raw.githubusercontent.com/Morris135212/COMS4111_project/main/app/static/images/User.png)

By clicking on Follower button, we can see all the followers for this user. To be mentioned, this is also one of the interesting queries we provide for part 2. By providing the user id of current user, we can check all followers of this user, and present that information.

For example, the following image shows that current user  only have 1 followers.

![Followers](https://raw.githubusercontent.com/Morris135212/COMS4111_project/main/app/static/images/Followers.png)
