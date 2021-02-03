# Simple blog site on Django

## Project features:
1. All features of simple blog app (creating posts, likes on posts, post comments, tags)
1. Elements of social networks (user pages, private messages between users)
1. Settings (each user can change their profile information in the settings, including changing the password, etc.)
1. User registration with email verification
1. Admin features (admin panel with opportunity to send email message to all users, post and comment moderation)
1. Delayed post publication for users

## Technology features
1. Related models with db indices
1. Authentication only by Django native resources for learning purposes
1. Queue of sending email messages with multiprocessing
1. Email messages are created by jinja template
1. User email verification by tokens
1. Project testing with pytest (fixtures, parametrize, etc.)
1. Logging to console and file
1. Custom template tag