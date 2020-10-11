UNTRUSTED_LIBRARIES = [
    # Mettre les editions a bannir ici
]

# Fields a avoir au minimum pour considerer le livre comme valide
# Regarder le nom des fields dans leslibraires/items.py
REQUIRED_FIELDS = [
    "title",
    "author",
    "description",
    "ean13"
]

# Nombre de pages maximum a crawler (-1 = illimite)
MAX_PAGES = -1

# Urls de base
BASE_URL = "https://www.leslibraires.fr"
RAYON_BASE_URI  = "/rayon"

# Noms des rayons (fin de l'url)
RAYONS = [
    "litterature",
    "arts-et-beaux-livres",
    "livres-pour-enfants",
    "livres-pratiques",
    "scolaire-et-universitaire",
    "savoirs",
    "policiers-science-fiction-fantasy",
    "bd-comics-mangas",
    "livres-pour-enfants",
    "romans-adolescents-jeunes-adultes",
]

# filtres a appliquer sur chaque rayon
# (pour les trouver, selectionner tous les filtres et copier l'url a partir du '?')
RAYON_FILTERS = "?f_price=5%2710%7C10%2720%7C20%2740%7C40%27-&f_shipping_delay=1"

# Don't touch this

RAYONS_BASE_URL = BASE_URL + RAYON_BASE_URI
START_URLS = []

for rayon in RAYONS:
    url = RAYONS_BASE_URL + "/" + rayon + RAYON_FILTERS
    START_URLS.append(url)

UNTRUSTED_LIBRARIES = list(map(lambda s: s.lower(), UNTRUSTED_LIBRARIES))

