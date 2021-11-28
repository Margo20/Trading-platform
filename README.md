# 'Trading platform' task implementation.
### Content/Instruments:
Authorization (jwt token), celery, redis, docker, docker-compose
### Usage:
For authorization use JSON like this:
```
{
    "user": {
        "username": "user1",
        "email": "user1@user.user",
        "password": "qweasdzxc"
    }
}
```