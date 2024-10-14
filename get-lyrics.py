import os
import requests
from bs4 import BeautifulSoup

# Function to generate Genius URL from artist and song name
def create_genius_url(artist, song_title):
    # Convert to lowercase, replace spaces with dashes
    artist = artist.lower().replace(' ', '-')
    song_title = song_title.lower().replace(' ', '-')
    
    # Remove special characters (apostrophes, punctuation, etc.)
    artist = re.sub(r'[^\w-]', '', artist)
    song_title = re.sub(r'[^\w-]', '', song_title)
    
    return f"https://genius.com/{artist}-{song_title}-lyrics"

# Function to scrape lyrics from Genius
def get_lyrics(artist, song_title):
    url = create_genius_url(artist, song_title)
    try:
        # Make the request to the Genius page
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Error: Genius page not found for {artist} - {song_title}")

        # Parse the page content
        soup = BeautifulSoup(response.content, 'lxml')
        # Genius uses a div with the class 'lyrics' or sometimes annotated text within 'p' tags
        lyrics = soup.find('div', class_='lyrics') or soup.find_all('p')
        
        if not lyrics:
            raise Exception(f"Error: Could not find lyrics for {artist} - {song_title}")

        # Extract lyrics text from div/p elements
        if isinstance(lyrics, list):  # When lyrics are in <p> tags
            lyrics = '\n'.join([verse.get_text() for verse in lyrics])
        else:
            lyrics = lyrics.get_text()

        # Save the lyrics to a text file
        file_name = f"{artist}-{song_title}.txt".replace(' ', '_')
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(lyrics.strip())

        print(f"Lyrics saved to {file_name}")

    except Exception as e:
        # Log the error into error.txt
        with open('error.txt', 'a', encoding='utf-8') as f:
            f.write(f"{artist} - {song_title}: {str(e)}\n")
        print(f"Error: {e}")

if __name__ == '__main__':
    songs = [
        ("Sabrina Carpenter", "emails i can't send"),
        ("Taylor Swift", "tis' the damn season"),
        ("Taylor Swift", "Bad Blood"),
        ("Olivia Rodrigo", "drivers license"),
        ("Ed Sheeran", "Shape of You"),
        ("Adele", "Hello"),
        ("The Weeknd", "Blinding Lights"),
        ("Billie Eilish", "bad guy"),
        ("Dua Lipa", "Levitating"),
        ("Harry Styles", "Watermelon Sugar"),
        ("Drake", "God's Plan"),
        ("Bruno Mars", "Uptown Funk"),
        ("Doja Cat", "Say So"),
        ("Lorde", "Royals"),
        ("Beyoncé", "Halo"),
        ("Ariana Grande", "thank u, next"),
        ("Sam Smith", "Stay With Me"),
        ("Katy Perry", "Firework"),
        ("Lady Gaga", "Shallow")
    ]

    
    for artist, song in songs:
        get_lyrics(artist, song)
