#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from array import array


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO Done: connect to a local postgresql database - URI in config.py

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.String(120))
    #seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    show = db.relationship('Show', backref='Venue', lazy=True)
    num_upcoming_shows = db.Column(db.Integer)

    
    # TODO Done: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    website_link = db.Column(db.String(120))
    #seeking_venue = db.Column(db.String(120))
    #seeking_description = db.Column(db.String(120))
    show = db.relationship('Show', backref='Artist', lazy=True)
    num_upcoming_shows = db.Column(db.Integer)



    #ToDo: Done Add [fb] seeking_venue and seeking_description [img] 

    # TODO Done: implement any missing fields, as a database migration using Flask-Migrate

# TODO Done: Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(str(value))
  #date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')
  #return babel.dates.format_datetime(str(date, format, locale='en'))

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
  # TODO: Done replace with real venues data.
  # DONE     num_shows should be aggregated based on number of upcoming shows per venue.
  
  # Returns state, city & venues. Needs # of upcoming shows DONE
  areas = Venue.query.distinct('city','state').all()
  data=[]
  num_upcoming_shows = []
  num_past_shows = []
  for area in areas:
    area.venues = Venue.query.filter(Venue.city == area.city, Venue.state == area.state).all()
    for venue in area.venues:
      venue.id = Venue.id
      venue.name = Venue.name
      #shows past & upcoming
      shows = Show.query.filter_by(id=venue.id).all()
      for show in shows:
        if show.start_time > datetime.today():
          num_upcoming_shows = len(shows)
        
        elif show.start_time < datetime.today():
          num_past_shows = len(shows)
          
        venues_detail = {
          'city': area.city,
          'state': area.state,
          'venues': [{
            "venue.id": venue.id, 
            "venue.name": venue.name, 
            "num_upcoming_shows": num_upcoming_shows 
            }],
          }
        data.append(venues_detail) 
    
  return render_template('pages/venues.html', areas = areas, venues = data)
  
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  #get input, search Venue
 
 
 
 ''' DUMMY DATA
 response={-
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))
'''
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id in venues.html
  # TODO: DONE replace with real venue data from the venues table, using venue_id
  
  #venue id
  venue = Venue.query.get(venue_id)
  shows = Show.query.filter_by(venue_id=Show.venue_id).all()

  #Shows - past and future
  past_shows = []
  upcoming_shows = []
  for show in shows:
    if show.start_time < datetime.now():
      past_shows.append({
        "artist_id": show.artist_id,
        "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
        "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
        "start_time": format_datetime(show.start_time)
      })
    elif show.start_time > datetime.now():
      upcoming_shows.append({
          "artist_id": show.artist_id,
          "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
          "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
          "start_time": format_datetime(show.start_time)
        })
  #TODO Done shows info; working on it
  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  
  return render_template('pages/show_venue.html', venue = data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: DONE insert form data as a new Venue record in the db, instead
  # *TODO: modify data to be the data object returned from db insertion

  form = VenueForm()
  
  venue = Venue(
    name = request.form['name'],
    city = request.form['city'],
    state = request.form['state'],
    address = request.form['address'],
    phone = request.form['phone'],
    image_link = request.form['image_link'],
    facebook_link = request.form['facebook_link'],
    genres = request.form.getlist('genres'),
    website_link = request.form['website_link'],
    seeking_talent = request.form['seeking_talent'],
    seeking_description = request.form['seeking_description'],    
  )
 
  try:
    db.session.add(venue)
    db.session.commit()
    # TODO Done: on successful db insert, flash success
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/ 
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except Exception as e:
    db.session.rollback()
    print(e)
    # TODO Done: on unsuccessful db insert, flash an error instead.
    flash('Problem: Venue ' + request.form['name'] + ' could not be added.')  

  finally:
    db.session.close()
  return render_template('pages/venues.html')
  #ex: return render_template('pages/shows.html', shows=data)
  
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: Done replace with real data returned from querying the database
  # for artist in artists | artist.id  | artist.name

  artists = Artist.query.all()
  for artist in artists:
    artist.id = artist.id
    artist.name = artist.name
  
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: ***Trouble*** implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  #search_term, results.count, results.data
  search = '%{}%'.format(request.form.get('search_term'))

  artists = Artist.query.filter(Artist.name.ilike(search)).all


  for artist in artists:
    response = {
      "count": len(search),
      "id": artist.id,
      "name": artist.name,
      #"num_upcoming_shows": Artist.num_upcoming_shows
    }
    
    '''
    response={
      "count": 1,
      "data": [{
        "id": 4,
        "name": "Guns N Petals",
        "num_upcoming_shows": 0,
      }]
    }
    '''
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id (show_artist, )
  # TODO: replace with real venue data from the venues table, using venue_id
  
  #Learning from: No display in upcoming shows and past shows
  #artist = Artist.query.filter_by(id=artist_id).first()
  artist = Artist.query.get(artist_id)
  shows = Show.query.filter_by(artist_id=Show.artist_id).all()
  
  #Shows past & future
  past_shows = []
  upcoming_shows = []
  for show in shows:
    if show.start_time < datetime.now():
      past_shows.append({
        "artist_id": show.artist_id,
        "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
        "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
        "start_time": format_datetime(show.start_time)
      })
    elif show.start_time > datetime.now():
      upcoming_shows.append({
          "artist_id": show.artist_id,
          "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
          "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
          "start_time": format_datetime(show.start_time)
        })
    
  data = {
    "id": show.artist_id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website_link": artist.website_link,
    "facebook_link": artist.facebook_link,
    #"seeking_venue": artist.seeking_venue,
    #"seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  return render_template('pages/show_artist.html', artist=data)
  
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = ArtistForm()

  artist=Artist(
    name = request.form['name'],
    city = request.form['city'],
    state = request.form['state'],
    phone = request.form['phone'],
    image_link = request.form['image_link'],
    facebook_link = request.form['facebook_link'],
    genres = request.form.getlist('genres'),
    website_link = request.form['website_link'],
    #show = request.form['show'],
    #num_upcoming_shows = request.form['num_upcoming_shows'],
  )

  print(artist)

  try:
    db.session.add(artist)
    db.session.commit()
  
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  
  except Exception as e:
    db.session.rollback()
    print(e)
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('Problem: Artist ' + request.form['name'] + ' could not be listed.')
  
  finally:
    db.session.close()
  return render_template('pages/home.html')
  return render_template('pages/shows.html', shows=data)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: PROBLEMS replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  data = []
  shows = Show.query.join(Venue, Show.venue_id == Venue.id).join(Artist, Artist.id == Show.artist_id).all()
  for show in shows:
    #num_shows upcoming shows per venue
    if show.start_time > datetime.today():
      num_upcoming_shows = len(shows)
      #venue
      venues = Venue.query.filter_by(id=Show.venue_id).all() #each show has venue
      for venue in venues:
        show.venue_id = Show.venue_id
        show.venue_name = Venue.name
         
      #artist
      artists = Artist.query.filter_by(id=Show.artist_id).all()
      for artist in artists:
        show.artist_id = Show.artist_id
        show.artist_name = Artist.name
        show.artist_image_link = Artist.image_link 


      '''
      #format for html template
      show.venue_id = Show.venue_id
      show.venue_name = Venue.name
      show.artist_id = Show.artist_id
      show.artist_name = Artist.name
      show.artist_image_link = Artist.image_link 
      #show.start_time = show.start_time
      '''

    
      show_detail = {
        "venue_id": show.venue_id,
        "venue_name": show.venue_name,
        "artist_id": show.artist_id,
        "artist_name": show.artist_name,
        "artist_image_link": show.artist_image_link,
        "start_time": format_datetime(show.start_time)
      }
      data.append(show_detail)
            
    #show.start_time.strftime("%m/%d/%Y, %H:%M")
    #datetime.strptime(show.start_time, "%m/%d/%Y, %H:%M")

  return render_template('pages/shows.html', shows=data)
  


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  form = ShowForm()
  #form = ShowForm(request.form) from how to insert data into show table

  show = Show(
    venue_id = request.form['venue_id'],
    artist_id = request.form['artist_id'],
    start_time = request.form['start_time']
  )

  print(show)

  try:
    db.session.add(show)
    db.session.commit() 
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  
  except Exception as e:
    db.session.rollback()
    print(e)  
  # TODO: DONE on unsuccessful db insert, flash an error instead.
    flash('Problem: Show for ' + request.form['start_time'] + ' could not be added.')  

  finally:
    db.session.close()
  return render_template('pages/shows.html')
  #return render_template('pages/shows.html', show=show)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
