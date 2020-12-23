# Todo Site
This is a fully functioning Todo site. Some of the site features include:
* Full CRUD control over your Todos. This means that you can:
  * Create your Todo
  * Check your Todo
  * Change your Todo
  * Complete or delete your Todo

* Fully working authentication system: I'm using Django's built in auth system, and this means:
  * Your passwords are encrypted with SHA256.
  * Your account credentials are safely stored in a PostgreSQL database.
  * If you create an account with email address, you need to verify it!

* User Profile. This means that you can:
  * Update it with your cool avatar
  * you can give it a bio. Something memorable, or just how you feel today :)
  * And finally you can check others' people profile! And don't worry about the email field in your User Profile page! It's visible to only you.

* Fully working Dark Mode:
  * This project has fully working Dark Mode. You just need to turn it on from the settings!
  * It's using DarkReader JS code to generate dynamically dark page. It's sooo convenient!

* Some miscellaneous stuff:
  * Query string handling with templatetag.
  * I made it really simple for administrators to handle the site traffic.
  * Password reset feature.
  * There are other things that make up my site, but the ```README``` will become too bloated.

You can find the deployed project on this url: https://www.mk-todos.cf<br>
EDIT: I stopped the web server because of security issues. Expect in the future a new deployment!

```
SOME NOTES:
  * I love privacy, so everything I do is privacy friendly. If some feature is bothering you, don't hesitate to contact me!
    * You can choose not to enter your email address. Doing so, you lose the functionality to reset your password, if needed someday!
    * When you delete your profile, EVERYTHING that you had in the database is gone forever. Nothing is disabled or hidden. Everything is deleted.
```
