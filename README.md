Technologies: Python, Django, REST APIs, GitHub.

Objective: Integrate GitHub with a Django application via the GitHub REST API.

Environment setup:

Register an oAuth application from your Github account
Create a dummy repository on your Github profile for this assignment - We’ll get to what you should do with this later.
Use:
  1. Django
  2. PostgreSQL
  3. Django ORM

Past this, it's all up to you.

Specifications - Start with the first and progress downwards. It should work out that way anyways.

1. I should be able to register as a user and then login to the application.
    1. Use the standard Django auth models for user management. Keep it simple - name, username, password.
3. After logging in, I should see a Link GitHub account button.
    1. On clicking this, I should be asked to authorize your app (remember the one you created in Step 2 of setup) to access my Github account. If you've never done this, it's a page hosted by GH, you don't need to build anything for the oauth.
5. Persist my oAuth credentials in the db.
6. After I authorize, I should be provided with a list of my public repositories on Github and given an option to select one.
7. Store this selection in the db.
8. When I select one, set up web hooks on that repository that will relay any events on the repository, specifically, pull request merged and code pushed to an URL endpoint on the Django app.
9. Create this URL endpoint that accepts the web hooks from my repo and store the event payload in the db.
10. Show me a list of all the web hooks events received from my repo in another page.

You are free to integrate directly with the API or use any of the Github python wrappers available.

This is probably more than 2 or 3 hours of work, if you want to finish it out
you're more than welcome, but don't fret about stopping at 2.5 hours. This is
a basis of a conversation about how you went about this, the steps you tooks,
the decisions you made etc.

Please create a public repo on your GH account and push this work to it. Email me when you are finished, we will schedule a time to touch base about it in the near future.
