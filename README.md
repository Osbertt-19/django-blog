# Django Blog

## Features added

### Models

- Blog posts
- Comments
- Tags(a custom tag model and it's a bit dysfunctional at the abstraction layer,works fine at the user interface tho. I might try django-taggit later.)

### CRUD functions

- Create posts,comments,tags
- Retrieve posts,comments,tags with List view(providing pagination and "draft post" section) and Detail view
- Update posts,tags
- Delete posts

### Authentication functions

- Sign up
- Log in
- Log out

### Share function

- via email

### Filter functions

- by Author
- by Tag

### Search function

- Basic search

### API

- Rest api for posts,comments and tags
