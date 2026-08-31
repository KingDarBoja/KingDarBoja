import os
import urllib.request
import urllib.parse

BADGES = {
    "languages": [
        ("TypeScript", "3178C6", "typescript", "white"),
        ("JavaScript", "F7DF1E", "javascript", "black"),
        ("Python", "3776AB", "python", "white"),
        ("Dart", "0175C2", "dart", "white"),
        ("Java", "ED8B00", "openjdk", "white"),
        ("Scala", "DC322F", "scala", "white"),
        ("HTML5", "E34F26", "html5", "white"),
        ("CSS3", "1572B6", "css", "white"),
        ("Sass", "CC6699", "sass", "white"),
        ("SQL", "4479A1", "sqlite", "white"),
    ],
    "frontend": [
        ("Angular", "DD0031", "angular", "white"),
        ("RxJS", "B7178C", "reactivex", "white"),
        ("NgRx", "BA2BD2", "ngrx", "white"),
        ("Apollo Angular", "311C87", "apollographql", "white"),
        ("React", "61DAFB", "react", "white"),
        ("Next.js", "000000", "nextdotjs", "white"),
        ("TailwindCSS", "38B2AC", "tailwindcss", "white"),
        ("Material UI", "007FFF", "materialdesign", "white"),
        ("Flutter", "02569B", "flutter", "white"),
        ("Jaspr", "0175C2", "dart", "white"),
        ("Three.js", "000000", "threedotjs", "white"),
        ("D3.js", "F9A03C", "d3dotjs", "white"),
    ],
    "backend": [
        ("NodeJS", "43853D", "nodedotjs", "white"),
        ("Flask", "000000", "flask", "white"),
        ("FastAPI", "009688", "fastapi", "white"),
        ("GraphQL", "E10098", "graphql", "white"),
        ("PostgreSQL", "316192", "postgresql", "white"),
        ("MongoDB", "47A248", "mongodb", "white"),
        ("NumPy", "013243", "numpy", "white"),
        ("Pandas", "150458", "pandas", "white"),
        ("Seaborn", "3776AB", "python", "white"),
        ("Matplotlib", "11557C", "python", "white"),
        ("PySpark", "E25A1C", "apachespark", "white"),
        ("Databricks", "FF3621", "databricks", "white"),
        ("Postman", "FF6C37", "postman", "white"),
    ],
    "cloud_devops": [
        ("GCP", "4285F4", "googlecloud", "white"),
        ("AWS", "232F3E", "amazonwebservices", "white"),
        ("Firebase", "FFCA28", "firebase", "black"),
        ("Docker", "2496ED", "docker", "white"),
        ("GitHub Actions", "2088FF", "githubactions", "white"),
        ("Git", "F05032", "git", "white"),
    ],
    "tools": [
        ("ESLint", "4B32C3", "eslint", "white"),
        ("Prettier", "F7B93E", "prettier", "black"),
        ("uv", "DE5FE9", "astral", "white"),
        ("Black", "000000", "black", "white"),
        ("Ruff", "D7FF64", "ruff", "black"),
        ("NPM", "CB3837", "npm", "white"),
        ("Yarn", "2C8EBB", "yarn", "white"),
        ("NVM", "333333", "nvm", "white"),
        ("Jupyter", "F37626", "jupyter", "white"),
        ("Conda", "44A833", "anaconda", "white"),
        ("GitHub Copilot", "000000", "githubcopilot", "white"),
        ("Google Gemini", "8E75B2", "googlegemini", "white"),
    ],
    "learning": [
        ("FastAPI", "009688", "fastapi", "white"),
        ("MongoDB", "47A248", "mongodb", "white"),
        ("Databricks", "FF3621", "databricks", "white"),
        ("PySpark", "E25A1C", "apachespark", "white"),
        ("Scala", "DC322F", "scala", "white"),
        ("Agentic AI", "6C5CE7", "openai", "white"),
    ],
    "social": [
        ("LinkedIn", "0A66C2", "linkedin", "white"),
        ("GitHub", "181717", "github", "white"),
        ("Portfolio", "4F46E5", "googlechrome", "white"),
    ]
}

def sanitize_filename(name):
    return name.lower().replace(" ", "-").replace(".", "").replace("/", "-")

def download_badges():
    base_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "badges")
    os.makedirs(base_dir, exist_ok=True)
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for category, badge_list in BADGES.items():
        cat_dir = os.path.join(base_dir, category)
        os.makedirs(cat_dir, exist_ok=True)
        
        for label, bg_color, logo, logo_color in badge_list:
            slug = sanitize_filename(label)
            file_path = os.path.join(cat_dir, f"{slug}.svg")
            
            # Format: https://img.shields.io/badge/-<Label>-<Color>?style=flat-square&logo=<Logo>&logoColor=<LogoColor>
            encoded_label = urllib.parse.quote(f"-{label}")
            url = f"https://img.shields.io/badge/{encoded_label}-{bg_color}?style=flat-square&logo={logo}&logoColor={logo_color}"
            
            print(f"Downloading [{category}] {label} from {url}...")
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req) as resp:
                    content = resp.read()
                    with open(file_path, "wb") as f:
                        f.write(content)
                print(f"Saved to {file_path}")
            except Exception as e:
                print(f"Failed for {label}: {e}")

if __name__ == "__main__":
    download_badges()
