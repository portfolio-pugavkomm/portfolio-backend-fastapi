# portfolio-backend-fastapi

A repository with a backend portfolio on fast api. Written with the purpose of repeating and learning new things in fast
api, since I have been working only with djnago for a long time.

## Main idea

The idea of this project is incredibly simply and consists of simple training of my skills, as well as restoration of
knowledge on working with fastapi, since for a long time I worked mainly with django.

The portfolio project should include the ability to register and authorize users. A little admin panel (just for me).
Obviously, JWT tokens will be used for authentication.

## System design

- Monolith structure
- valkey cache
- Celery (or not?)

## Database

Classic postgreSQL.

## Cache

Valkey

## [Changelog](CHANGELOG.md)

## [Developer guide](mds/Developer_guide.md)

## TODO

-[x] Init project
-[x] Configure mypy, black etc.
-[ ] Create developer and style guide
-[ ] Docker + docker-compose configuration with database. (develop)
-[ ] Deploy + docker + docker-compose configuration with database (production)
-[ ] CI-CD pipline with github actions
-[ ] Main part api about me
-[ ] Customers part api
-[ ] Some happy parts with experiments