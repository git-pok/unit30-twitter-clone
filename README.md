# Unit30 Twitter Clone Collaborative Project
This was a collaborative project. Please read each file to see what logics and files I created. Read "My Project Tasks" to see what I had to solve for.

# My Project Tasks
## Part One: Fix Current Features
### Step One: Understand the Model
Read models.py. Make a diagram of the four tables.

### Step Two: Fix Logout
Right now, there are links in the site to logout, but the logout route is not implemented.
On logout, it should flash a success message and redirect to the login page.

### Step Three: Fix User Profile
The profile page for users works, but is missing a few things:
- the location
- the bio
- the header image (which should be a background at the top)

Add these.

### Step Four: Fix User Cards
On the followers, following, and list-users pages, the user cards need to show the bio for the users. Add this.

### Step Five: Profile Edit
There are buttons throughout the site for editing your profile, but this is unimplemented.

It should ensure a user is logged on (you can see how this is done in other routes)

It should show a form with the following:
- username
- email
- image_url
- header_image_url
- bio
- password [see below]

It should check that that password is the valid password for the user—if not, it should flash an error and return to the homepage.

It should edit the user for all of these fields except password ie, this is not an area where users can change their passwords–the password is only for checking if it is the current correct password.

On success, it should redirect to the user detail page.

### Step Six: Fix Homepage
The homepage for logged-in-users should show the last 100 warbles only from the users that the logged-in user is following, and that user, rather than warbles from all users.

### Step Seven: Research and Understand Login Strategy
Look over the code in app.py related to authentication.

How is the logged in user being kept track of?
What is Flask’s g object?
What is the purpose of add_user_to_g?
What does @app.before_request mean?

## Part Two: Add Likes
Add a new feature that allows a user to “like” a warble. They should only be able to like warbles written by other users. They should put a star (or some other similar symbol) next to liked warbles.

They should be able to unlike a warble, by clicking on that star.

On a profile page, it should show how many warblers that user has liked, and this should link to a page showing their liked warbles.

## Part Three: Add Tests
Add tests. You’ll need to proceed carefully here, since testing things like logging in and logging out will need to be tested using the session object.

We created some (mostly empty) test files:

test_user_model.py
test_user_views.py
test_message_model.py
test_message_views.py