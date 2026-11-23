# CsHub: Requirements


## 1. Problem
Students of the CS department currently ask their questions in Facebook groups. In these groups, posts about every topic are mixed together, so a question is quickly buried under newer posts, and old answers are hard to find. As a result, the same questions are asked again and again, and the experience of each cohort is lost when it graduates. Some students also do not use Facebook, so they are left out. The department needs an organized, searchable platform made only for its students.


## 2. Users
- Student: creates posts (questions), comments on posts (answers), likes posts, searches, and reports inappropriate posts.
- Admin: approves new accounts, creates the communities, deactivates bad users, and deletes bad posts and comments.

## 3. Functional requirements

### Accounts
- FR1: The system shall allow a visitor to register an account with a username, email, and password.
- FR2: The system shall keep a new account inactive until the admin approves it in the admin panel.
- FR3: The system shall allow an approved student to log in and log out.

### Communities
- FR4: The system shall allow the admin to create, edit, and delete communities (Courses and Study, Teachers, Graduation Projects, Student Life).
- FR5: The system shall display the list of communities on the home page.
- FR6: The system shall display the posts of a community on its own page.

### Posts
- FR7: The system shall allow a logged-in student to create a post with a title, a body, and a community.
- FR8: The system shall allow any visitor to read posts.
- FR9: The system shall allow the author of a post to edit it.
- FR10: The system shall allow the author of a post to delete it.

### Comments
- FR11: The system shall allow a logged-in student to add a comment to a post.
- FR12: The system shall display the comments under each post, from oldest to newest.

### Likes
- FR13: The system shall allow a logged-in student to like a post, only once per post.
- FR14: The system shall display the number of likes on each post.

### Search
- FR15: The system shall allow a user to search posts by a keyword in the title or body.

### Reports and moderation
- FR16: The system shall allow a logged-in student to report a post with a reason.
- FR17: The system shall allow the admin to review reports and delete reported posts through the admin panel.
- FR18: The system shall allow the admin to deactivate a user account.
- FR19: The system shall allow the admin to delete any comment.

## 4. Non-functional requirements

- NFR1 (Language): The system shall store and display text in Arabic, French, and English correctly.
- NFR2 (Security): The system shall store passwords hashed and never as plain text.
- NFR3 (Access control): The system shall allow only logged-in and approved users to create posts, comments, likes, and reports.
- NFR4 (Ownership): The system shall allow only the author of a post to edit or delete it, and the admin to delete any post.
- NFR5 (Usability): The system shall display correctly on both computer and phone screens.
- NFR6 (Performance): The system shall load any page in under 3 seconds under normal use.
- NFR7 (Reliability): The system shall keep all data in the MySQL database, so nothing is lost when the server restarts.
- NFR8 (Maintainability): The code shall be stored in a Git repository with a clear commit history.
- NFR9 (Protection of input): The system shall escape user text on display, so that scripts typed in a post do not run.

## 5. Out of scope
- Nested replies (a reply to a comment)
- Downvotes
- Notifications
- Bookmarks (saving posts)
- Tags
- AI search
- A moderator role
- Email verification

These are possible future work.
## 6. Constraints
- One developer, with a fixed deadline set by the university.
- Free tools only, and demo-only hosting.
- Only students of the CS department can use the platform.
- Web application only, with no mobile app.
