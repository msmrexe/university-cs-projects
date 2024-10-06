% Maryam Rezaee (981813088) - MATLAB Mini Golestan Project


% -------------------------- INITIALISING DATA ----------------------------

% employees = [username password]
employees = [401101 1001; 401102 1002];

% teachers = [username password]
teachers = [401201 2001; 401202 2002; 401203 2003];

% students = [username password grade*5]
% pending grades are stored as -1
students = [401301 3001 -1 -1 15 -1 -1;
    401302 3002 -1 -1 13.25 -1 -1;
    401303 3003 -1 -1 19 -1 -1;
    401304 3004 -1 -1 20 -1 -1;
    401307 3007 -1 -1 16 -1 -1;
    401308 3008 -1 -1 18 -1 -1;
    401305 3005 -1 -1 18.75 -1 -1;
    401306 3006 -1 -1 15 -1 -1;
    401309 3009 -1 -1 17.5 -1 -1;
    401310 3010 -1 -1 20 -1 -1;
    401311 3011 -1 -1 20 -1 -1;
    401312 3012 -1 -1 11.5 -1 -1;
    401313 3013 -1 -1 17 -1 -1;
    401314 3014 -1 -1 10 -1 -1;
    401315 3015 -1 -1 20 -1 -1;
    401316 3016 -1 -1 8.5 -1 -1;
    401317 3017 -1 -1 19.75 -1 -1;
    401318 3018 -1 -1 9.25 -1 -1;
    401319 3019 -1 -1 10.25 -1 -1;
    401320 3020 -1 -1 12.75 -1 -1];

% courses = [credits min max avg]
courses = [3 assess(students, 3);
    3 assess(students, 4);
    3 assess(students, 5);
    3 assess(students, 6);
    4 assess(students, 7)];


% ------------------------------ MAIN BODY --------------------------------


% looping the general menu to make returning possible
while true

    fprintf("Welcome to Mini Golestan!\n" + ...
        "Which type of user are you?\n" + ...
        "- Employee: e\n" + ...
        "- Teacher: t\n" + ...
        "- Student: s\n");
    type = input("Type the respective letter to access your portal: ", "s");

    % getting valid username
    username = input("Enter your username: ");
    ongoing = true;
    while ongoing
        if type == "e"
            status = search(employees, username, 1);
        elseif type == "t"
            status = search(teachers, username, 1);
        elseif type == "s"
            [status, idx] = search(students, username, 1);
        end
        if status == false
            username = input("Wrong username! Try again: ");
        else
            ongoing = false;
        end
    end

    % getting valid password
    password = input("Enter your password: ");
    ongoing = true;
    while ongoing
        if type == "e"
            status = search(employees, password, 2);
        elseif type == "t"
            status = search(teachers, password, 2);
        elseif type == "s"
            [status, idx] = search(students, password, 2);
        end
        if status == false
            password = input("Wrong password! Try again: ");
        else
            fprintf("You're in!\n\n")
            ongoing = false;
        end
    end

    % looping each portal's menu to make returning possible
    while true

        % employee portal
        if type == "e"
            fprintf("Menu Options:\n" + ...
                "0) Exit Portal\n" + ...
                "1) Course Details: Design and Analysis of Algorithms\n" + ...
                "2) Course Details: Fundamentals of Numerical Analysis\n" + ...
                "3) Course Details: Mathematics Databases\n" + ...
                "4) Course Details: Mathematics Softwares\n" + ...
                "5) Course Details: Principles of Operating Systems\n");
            num = input("Enter option number: ");
            if num == 0
                fprintf("Exiting employee portal...\n\n");
                break
            else
                fprintf("\nCurrent course credits: %d\n", courses(num, 1));
                action = input("Would you like to edit credits? (y/n): ", "s");
                if action == "y"
                    new = input("Enter new course credits: ");
                    courses(num, 1) = new;
                    fprintf("Credits updated successfully! Returning you to menu...\n\n");
                else
                    fprintf("Alright! Returning you to menu...\n\n");
                end
            end

        % teacher portal
        elseif type == "t"
            fprintf("Menu Options:\n" + ...
                "0) Exit Portal\n" + ...
                "1) Course Details: Design and Analysis of Algorithms\n" + ...
                "2) Course Details: Fundamentals of Numerical Analysis\n" + ...
                "3) Course Details: Mathematics Databases\n" + ...
                "4) Course Details: Mathematics Softwares\n" + ...
                "5) Course Details: Principles of Operating Systems\n");
            num = input("Enter option number: ");
            if num == 0
                fprintf("Exiting teacher portal...\n\n");
                break
            else
                if students(1, num+2) < 0
                    fprintf("Grades have not yet been entered! Enter them below:\n");
                    empty = true;
                else
                    empty = false;
                    fprintf("Student %d: %f\n", [students(:, 1), students(:, num+2)]');
                    fprintf("Min: %f\nMax: %f\nAverage: %f\n", courses(num, 2:end));
                    action = input("Would you like to edit the grades? (y/n): ", "s");
                end
                if empty || action == "y"
                    for i = 1:20
                        fprintf("Student Number: %d\n", students(i, 1));
                        new = input("Enter grade: ");
                        students(i, num+2) = new;
                    end
                    courses(num, 2:end) = assess(students, num+2);
                    fprintf("Grades saved successfully! Returning you to menu...\n\n");
                elseif action == "n"
                    fprintf("Alright! Returning you to menu...\n\n");
                end
            end

        % student portal
        elseif type == "s"
            titles = ["Design and Analysis of Algorithms"
                "Fundamentals of Numerical Analysis"
                "Mathematics Databases"
                "Mathematics Softwares"
                "Principles of Operating Systems"];
            fprintf("Menu Options:\n" + ...
                "0) Exit Portal\n" + ...
                "1) Course Details: Design and Analysis of Algorithms\n" + ...
                "2) Course Details: Fundamentals of Numerical Analysis\n" + ...
                "3) Course Details: Mathematics Databases\n" + ...
                "4) Course Details: Mathematics Softwares\n" + ...
                "5) Course Details: Principles of Operating Systems\n" + ...
                "6) Report Card\n");
            num = input("Enter option number: ");
            if num == 0
                fprintf("Exiting student portal...\n\n");
                break
            elseif num == 6
                fprintf("\n");
                for i = 1:5
                    if students(idx, i+2) >= 0
                        fprintf("%s: %f\n", titles(i), students(idx, i+2));
                    end
                end
                gpa = gpacalc(students, courses, idx);
                if not(isnan(gpa))
                    fprintf("GPA: %f\nReturning you to menu...\n\n", gpa);
                else
                    fprintf("No courses have grades yet.\n" + ...
                        "Returning you to menu...\n\n");
                end
            else
                if students(idx, num+2) >= 0
                    fprintf("\nYour grade for %s: %f\n", titles(num), students(idx, num+2));
                    action = input("Would you like to view more details? (y/n): ", "s");
                    if action == "y"
                        fprintf("\nMin: %f\nMax: %f\nAverage: %f\nReturning you to menu...\n\n", courses(num, 2:end));
                    else
                        fprintf("Alright! Returning you to menu...\n\n");
                    end
                else
                    fprintf("\nGrades for this course have not yet been entered.\n" + ...
                        "Returning you to menu...\n\n");
                end
            end
        end
    end
end


% ------------------------------ FUNCTIONS --------------------------------


% function to calculate min, max, and avg of each course
% only counts students with a mark for that course
% avg is NaN if course marks are not entered
function result = assess(students, col)
    min = 20;
    max = 0;
    sum = 0;
    n = 0;
    for i = 1:20
        if students(i, col) >= 0
            sum = sum + students(i, col);
            n = n + 1;
            if students(i, col) < min
                min = students(i, col);
            end
            if students(i, col) > max
                max = students(i, col);
            end
        end
    end
    avg = sum / n;
    result = [min max avg];
end


% fucntion to calculate GPA of each student
% only counts courses with a mark for that student
% GPA is NaN if no course marks are entered
function gpa = gpacalc(students, courses, row)
    points = 0;
    credits = 0;
    for i = 3:7
        if students(row, i) >= 0
            points = points + (students(row, i) * courses(i-2, 1));
            credits = credits + courses(i-2, 1);
        end
    end
    gpa = points / credits;
end


% function to search data for username or password
% the two types of search are specified using states
% state = 1 (username), state = 2 (password)
function [status, idx] = search(data, key, state)
    status = false;
    idx = 0;
    for i = 1:length(data)
        if data(i, state) == key
            status = true;
            idx = i;
        end
    end
end

