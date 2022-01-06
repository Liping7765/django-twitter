# django-twitter 

### **Backend Project – Twitter** [<img src='https://help.twitter.com/content/dam/help-twitter/brand/logo.png' alt='twitter' height='40'>]()

Summary: This project is to design, develop, and implement Restful APIs to operate Twitter-like backend service as close to real-world development as possible based on Django REST Framework. For performance optimization, structured and unstructured databases are implemented in this project according to the nature of the tables.

> **Tech Stack: Python, Django, MySQL, HBase, Redis, Memcached, RabbitMQ, Amazon S3**

- Optimized its responding time by using Message Queue to deliver newsfeeds as asynchronized tasks so server could have instant response to clients
- Leveraged Redis and Memcached to cache data for users and posts, reducing database queries for tables that need to be read in high frequency (eg. Users, Posts)
- Boosted the APIs response time with Key-Value HBase storage for tables with high volume of writings
- Utilized denormalization to keep a close track of counts of comments and likes for each post (e.g. likes_count, comments_count in Tweet table)
- Customized and created 20+ unit tests for each data model and feature to ensure its quality and feasibility


#### Features:

- User Authentification: Allow users to log in or sign up with emails 
- Allow users to follow, unfollow other users
- Allow users to view, comment, and like others' posts, also users can cancel their comments and likes on the posts
- Allow users to create, delete, update posts and view the count of likes and comments of their posts
- Send out newfeeds to followers

