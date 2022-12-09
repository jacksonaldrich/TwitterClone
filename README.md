# TwitterClone

### Functionalities of this site:

**Required Tasks:**
each required task being worth 5 points and corresponds to one of the routes on my webpage

1. Home
    1. a link to this page should always be visible in your menu, whether the user is logged in or not logged in
    1. this route displays all the messages in the system
    1. the messages should be ordered chronologically with the most recent message at the top
    1. each message should include the user account that created it, the time of creation, and the message contents
    1. at least one message must contain a single quote `'` and a double quote `"`

1. Log in
    1. a link to this page should only be visible in your menu if the user is not logged in
    1. this route will present a form for the user to enter their username/password;
       the password box must not display the user's password as they are typing it in
    1. you must display appropriate error messages if the user enters an incorrect username/password
    1. after a user successfully logs in, you must automatically redirect them to the homepage

1. Log out
    1. a link to this page should only be visible if the user is logged in
    1. this route will delete the cookies that the log in form creates, logging the user out


1. Create new user accounts
    1. a link to this page should only be visible in your menu if the user is not logged in
    1. if the user attempts to create an account that already exists, they should get an appropriate error message
    1. the user should be prompted to enter their password twice; if the passwords do not match, they should get an appropriate error message

1. Create a message
    1. a link to this page should only be visible in your menu if the user is logged in
    1. the user must be able to enter whatever message body they want,
       but you will also need to store the user id of the user that created a message and the time the message was created
    1. you will only get credit for this route if the message correctly shows up on the home route after creation  
    

**Optional Tasks pt. 1:**
the following tasks are worth 3 points each

1. Created a nicely themed webpage with HTML/CSS.
1. Added a json endpoint for my messages route that returns the list of messages in json format instead of HTML format.
1. Allow changing the password after creating an account. You must have a password reset form that forces the user to type in their old password and a new password twice.

**Optional Tasks pt. 2:**
the following tasks are worth 6 points each

1. Added the ability to search for messages.

**Optional Tasks pt. 3**
the following have different point values assigned

1. (0.5 points) formatted the "date_created" insert in a way that makes sense

**Total Grade:**
1. Required Tasks: 25
2. Optional Tasks: 15.5
### Total = 40.5
