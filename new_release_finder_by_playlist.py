import requests
import base64
import time
from datetime import datetime, timedelta, timezone

# --- Your Spotify API Credentials ---
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
# ------------------------------------

# --- Configuration ---
TARGET_USER_ID = "spotify"
# -----------------------------


def get_spotify_token(client_id, client_secret):
    """Gets an access token from the Spotify API."""
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')
    headers = {'Authorization': f'Basic {auth_header}'}
    data = {'grant_type': 'client_credentials'}
    response = requests.post(auth_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f"Error getting token: {response.status_code} - {response.text}")
        return None

def get_all_user_playlists(token, user_id):
    """Fetches all public playlists from a specific user's profile."""
    headers = {'Authorization': f'Bearer {token}'}
    all_playlists = []
    # This is the correct endpoint for getting a user's playlists
    next_url = f'https://api.spotify.com/v1/users/{user_id}/playlists?limit=50'

    print(f"Fetching all public playlists from user '{user_id}'... This will take a moment.")

    while next_url:
        response = requests.get(next_url, headers=headers)
        if response.status_code != 200:
            print(f"   > Error fetching playlist data: {response.status_code} - {response.text}")
            break

        data = response.json()
        all_playlists.extend(data.get('items', []))
        next_url = data.get('next')
        time.sleep(0.1)

    return all_playlists

def display_profile_playlists(playlists):
    """Displays the fetched playlists in a readable format."""
    if not playlists:
        print("Could not find any playlists for this user.")
        return

    print(f"\n--- 🎧 Found {len(playlists)} Playlists on Spotify's Profile ---")

    for i, playlist in enumerate(playlists, 1):
        name = playlist['name']
        playlist_id = playlist['id']
        # Truncate long descriptions for cleaner output
        description = (playlist['description'] or "No description.").replace('\n', ' ').strip()
        if len(description) > 100:
            description = description[:97] + "..."

        print(f"\n{i}. {name}")
        print(f"   ID: {playlist_id}")
        print(f"   Description: {description}")


if __name__ == "__main__":
    access_token = get_spotify_token(CLIENT_ID, CLIENT_SECRET)
    if access_token:
        spotify_playlists = get_all_user_playlists(access_token, TARGET_USER_ID)
        display_profile_playlists(spotify_playlists)
