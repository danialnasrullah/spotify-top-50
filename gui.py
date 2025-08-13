# gui.py
import customtkinter as ctk
from spotify import get_spotify_client, get_recent_tracks, get_user_display_name

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class SpotifyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Spotify GUI App")
        self.geometry("600x400")

        self.greeting_label = ctk.CTkLabel(self, text="Hello ...", font=("Arial", 20))
        self.greeting_label.pack(pady=10)
        self.label = ctk.CTkLabel(self, text="Your Recently Played Tracks", font=("Arial", 16))
        self.label.pack(pady=10)


        # Use a scrollable frame to hold track widgets
        self.tracks_frame = ctk.CTkScrollableFrame(self, width=560, height=250)
        self.tracks_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.button = ctk.CTkButton(self, text="Load Tracks", command=self.load_tracks)
        self.button.pack(pady=20)

    def load_image_for_label(self, img_label, image_url):
        import threading
        import urllib.request
        from PIL import Image
        import io
        from customtkinter import CTkImage

        def fetch_and_set_image():
            try:
                with urllib.request.urlopen(image_url) as u:
                    raw_data = u.read()
                im = Image.open(io.BytesIO(raw_data)).resize((50, 50))
                ctk_img = CTkImage(light_image=im, dark_image=im, size=(50, 50))
                
                def update_image():
                    if img_label.winfo_exists():  # Check if label still exists
                        img_label.configure(image=ctk_img)
                        img_label.image = ctk_img  # keep reference
                
                self.after(0, update_image)
            except Exception as img_e:
                def show_error():
                    if img_label.winfo_exists():
                        img_label.configure(text="[No Image]")
                self.after(0, show_error)

        thread = threading.Thread(target=fetch_and_set_image, daemon=True)
        thread.start()

    def load_tracks(self):
        import threading
        
        def fetch_tracks():
            try:
                sp = get_spotify_client()
                name = get_user_display_name(sp)
                tracks = get_recent_tracks(sp)
                print("Tracks fetched:", tracks)

                def update_gui():
                    self.greeting_label.configure(text=f"Hello {name}")
                    for widget in self.tracks_frame.winfo_children():
                        widget.destroy()
                    if tracks:
                        for i, track in enumerate(tracks, 1):
                            frame = ctk.CTkFrame(self.tracks_frame)
                            frame.pack(fill="x", padx=5, pady=3)

                            # Load and display image if available
                            img_label = ctk.CTkLabel(frame, text="Loading...")
                            img_label.pack(side="left", padx=5)
                            
                            # Start image loading in background
                            if track.get('image_url'):
                                self.load_image_for_label(img_label, track['image_url'])
                            else:
                                img_label.configure(text="[No Image]")

                            # Song info
                            info = f"{i}. {track['name']}\n{track['artist']} — {track['album']}"
                            info_label = ctk.CTkLabel(frame, text=info, anchor="w", justify="left")
                            info_label.pack(side="left", padx=10)

                            # Spotify link (if available)
                            if track.get('spotify_url'):
                                def open_url(url=track['spotify_url']):
                                    import webbrowser
                                    webbrowser.open(url)
                                link_btn = ctk.CTkButton(frame, text="Open in Spotify", width=120, command=open_url)
                                link_btn.pack(side="left", padx=10)
                    else:
                        ctk.CTkLabel(self.tracks_frame, text="No tracks found.").pack()

                self.after(0, update_gui)
            except Exception as e:
                def show_error():
                    for widget in self.tracks_frame.winfo_children():
                        widget.destroy()
                    ctk.CTkLabel(self.tracks_frame, text=f"Error: {e}").pack()
                self.after(0, show_error)

        threading.Thread(target=fetch_tracks, daemon=True).start()

if __name__ == "__main__":
    app = SpotifyApp()
    app.mainloop()
