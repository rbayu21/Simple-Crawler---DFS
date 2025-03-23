import requests
from bs4 import BeautifulSoup
import mysql.connector

# Konfigurasi database
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Ganti sesuai konfigurasi MySQL Anda
    password="",
    database="rangga"
)
cursor = db.cursor()

# Struktur DFS untuk menelusuri halaman
visited = set()

def dfs(url):
    if url in visited:
        print(f"Sudah dikunjungi: {url}")
        return
    print(f"Mengunjungi: {url}")
    visited.add(url)

    try:
        response = requests.get(url, timeout=5)  # Tambahkan timeout
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ambil judul halaman
        title = soup.title.string if soup.title else "No Title"

        # Ambil paragraf pertama
        paragraph = soup.find('p')
        content = paragraph.text if paragraph else "No Content"

        # Simpan ke database
        cursor.execute("INSERT INTO pages (url, title, content) VALUES (%s, %s, %s)", (url, title, content))
        db.commit()
        print(f"Disimpan: {url} | {title} | {content}")

        # Cari semua link dalam halaman
        for link in soup.find_all('a', href=True):
            next_url = f"http://localhost/{link['href']}"
            print(f"Menemukan link: {next_url}")  # Debugging
            dfs(next_url)

    except requests.exceptions.RequestException as e:
        print(f"Error mengambil {url}: {e}")

# Mulai DFS dari halaman index.html
dfs("http://localhost/index.html")

# Tutup koneksi database
cursor.close()
db.close()