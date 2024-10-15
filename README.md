Technologies: Python, Django, Vue, REST APIs, GitHub, Webhooks.

Objective: Integrate GitHub with a Django and Vue application via the GitHub and Google REST API.

Environment setup:

Register an oauth application from your Github account

Use:
  1. Django
  2. PostgreSQL
  3. Django ORM
  4. Django Request Framework for API Requests to the front-end
  5. Vue for a front end

Some tools that may be helpful:

https://github.com/guruahn/vue3-google-oauth2

Past this, it's all up to you. Considering time, I reccomend keeping most requests and logic on the front end and using the backend to store login and github credentials etc. 

Specifications - Start with the first and progress downwards. It should work out that way anyways.

On the front end:

1. I should be able to register as a user using Google OAuth and login to the application (don't worry too much about token auth, cookies, or state persistence for the login state). 
3. After logging in, I should see a Link GitHub account button.
    1. On clicking this, I should be asked to authorize your app to access my Github account. If you've never done this, it's a page hosted by GH, you don't need to build anything for the OAuth.
5. Persist the logged in users Github OAuth credentials in the db.
6. After I authorize, I should be provided with a list of my public repositories on Github and given an option to select one.
7. Store this selection in the db.

On the back-end:
1. You should have DRF views for proxying the requests from your front-end application to the Google OAuth API, as well as GitHub API.
2. Subscribe to webhook events for each repository found. Specifically we'd like to subscribe to: pull requests, merges, and code pushes.
3. Create a view / endpoint to receive / parse webhook events, but do not actually implement the processing of these events. We are only looking for an endpoint that will receive these events, no action needs to be taken once received.

You are free to integrate directly with the API or use any of the Google/Github python wrappers available. You can also use an OAuth provider plugin for the backend if you want to Oauth to the django application. Though, these decisions are up to you. 

This is probably more than 4 to 5 hours of work, if you want to finish it out
you're more than welcome, but don't fret about stopping at 3 or 4 hours. This is
a basis of a conversation about how you went about this, the steps you tooks,
the decisions you made etc.

Please create a public repo on your GH account and push this work to it. Email me when you are finished, we will schedule a time to touch base about it in the near future.
term