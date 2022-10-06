from .user import user_views
from .index import index_views
from .game import game_views
from .listing import listing_views
from .payment import payment_views
from .rental import rental_views

app_views = [
    user_views,
    index_views,
    game_views,
    listing_views,
    payment_views,
    rental_views,
]