
import os
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

ASSETS = [
    # CSS
    ("https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css", "css/bootstrap-4.4.1.min.css"),
    ("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css", "css/fontawesome-6.4.2.all.min.css"),
    ("https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css", "css/bootstrap-5.3.0.min.css"),
    ("https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css", "css/fontawesome-4.7.0.min.css"),
    ("https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.17.47/css/bootstrap-datetimepicker.min.css", "css/bootstrap-datetimepicker.min.css"),
    ("https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css", "css/jquery-ui.css"),
    ("https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css", "css/flatpickr.min.css"),

    # JS
    ("https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js", "js/jquery-3.7.1.min.js"),
    ("https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js", "js/bootstrap-bundle-5.3.0.min.js"),
    ("https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js", "js/bootstrap-bundle-5.1.3.min.js"),
    ("https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.8/umd/popper.min.js", "js/popper.min.js"),
    ("https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js", "js/bootstrap-bundle-5.3.2.min.js"),
    ("https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js", "js/bootstrap-4.4.1.min.js"),
    ("https://code.jquery.com/ui/1.12.1/jquery-ui.js", "js/jquery-ui.js"),
    ("https://cdn.jsdelivr.net/npm/flatpickr", "js/flatpickr.js"),
    ("https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js", "js/xlsx.full.min.js"),

    # Fonts (FA 6.4.2)
    ("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/webfonts/fa-solid-900.woff2", "webfonts/fa-solid-900.woff2"),
    ("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/webfonts/fa-brands-400.woff2", "webfonts/fa-brands-400.woff2"),
    ("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/webfonts/fa-regular-400.woff2", "webfonts/fa-regular-400.woff2"),
    
    # Fonts (FA 4.7.0)
    ("https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/fonts/fontawesome-webfont.woff2?v=4.7.0", "fonts/fontawesome-webfont.woff2"),
]

def download_file(url, relative_path):
    dest_path = os.path.join(STATIC_DIR, relative_path)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    print(f"Downloading {url} to {relative_path}...")
    try:
        # Add User-Agent headers to avoid some 403s
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req) as response, open(dest_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Success: {relative_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

if __name__ == "__main__":
    print(f"Starting download to {STATIC_DIR}")
    for url, path in ASSETS:
        download_file(url, path)
    print("Done.")
