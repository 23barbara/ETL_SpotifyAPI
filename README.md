# ETL_SpotifyAPI
With this project I wanted to simulate an ETL Process using python. 
Personal data is extracted using Spotify API, and then loaded into a Mongo Database.
The file main.py executes the whole ETL process which includes connecting to the Spotify API, getting user recently played songs and converting the information before storing it into the database.
The goal was to extract my recently played songs and have them saved.

I used my personal Spotify account in the project but kept it hidden for privacy (you can use your own username and generate a Token here if you want to try https://developer.spotify.com/console/get-recently-played/?limit=&after=&before=)

For help developing this personal project I used mainly @karolina-sowinska's data engineering for beginners course, besides MongoDB documentation and tutorials.
