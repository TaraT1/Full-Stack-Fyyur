Fyyur
-----

### Description

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

### Introduction

This project utililizes SQL And Data Modeling for the Web. 
* build CRUD app, implement data models in relational, normalized form using SQLAlchemy and SQL
* manage database schema using version control system with migration files
* connect data models to postgresql database
* join relational tables and conduct joined queries using SQL and SQLAlchemy


### Overview

Using a PostgreSQL database, this site is capable of:

* creating new venues as well as artists, and creating new shows.
* searching for venues and artists.
* learning more about a specific artist or venue.

The goal of Fyyur is to be a platform that artists and musical venues can use to find each other and audiences can discover new music shows. 

### Tech Stack

The tech stack includes:

* **SQLAlchemy ORM** is the ORM library 
* **PostgreSQL** is the database 
* **Python3** and **Flask** is the server language and server framework
* **Flask-Migrate** is used for creating and running schema migrations
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for the website's frontend

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app and includes SQLAlchemy models.
                    "python app.py" to run after installing dependencies
  ├── config.py *** Database URLs, CSRF generation, etc.
  ├── error.log
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies needed to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in the `MODELS` section of `app.py`.
* Controllers are also located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`


Highlight folders:
* `templates/pages` -- (Already defined.) Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `app.py`. These pages successfully represent the data to the user, and are already defined for you.
* `templates/layouts` -- (Already complete.) Defines the layout that a page can be contained in to define footer and header code for a given page.
* `templates/forms` -- (Already complete.) Defines the forms used to create new artists, shows, and venues.
* `app.py` -- (Missing functionality.) Defines routes that match the user’s URL, and controllers which handle data and renders views to the user. This is the main file you will be working on to connect to and manipulate the database and render views with data to the user, based on the URL.
* Models in `app.py` -- (Missing functionality.) Defines the data models that set up the database tables.
* `config.py` -- (Missing functionality.) Stores configuration variables and instructions, separate from the main application code. This is where you will need to connect to the database.


Instructions
-----

1. Understand the Project Structure (explained above) and where important files are located.
2. Build and run local development following the Development Setup steps below.
3. Fill in the missing functionality in this application: this application currently pulls in fake data, and needs to now connect to a real database and talk to a real backend.
3. Fill out every `TODO` section throughout the codebase. We suggest going in order of the following:

  1. Connect to a database in `config.py`. A project submission that uses a local database connection is fine.
  2. Using SQLAlchemy, set up normalized models for the objects we support in our web app in the Models section of `app.py`. Check out the sample pages provided at /artists/1, /venues/1, and /shows/1 for examples of the data we want to model, using all of the learned best practices in database schema design. Implement missing model properties and relationships using database migrations via Flask-Migrate.
  3. Implement form submissions for creating new Venues, Artists, and Shows. There should be proper constraints, powering the `/create` endpoints that serve the create form templates, to avoid duplicate or nonsensical form submissions. Submitting a form should create proper new records in the database.
  4. Implement the controllers for listing venues, artists, and shows. Note the structure of the mock data used. We want to keep the structure of the mock data.
  5. Implement search, powering the `/search` endpoints that serve the application's search functionalities.
  6. Serve venue and artist detail pages, powering the `<venue|artist>/<id>` endpoints that power the detail pages.

### Development Setup

First, [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask).

  ```
  $ cd ~
  $ sudo pip3 install Flask
  ```

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  $ python3 app.py
  ```

4. Navigate to Home page [http://localhost:5000](http://localhost:5000)
