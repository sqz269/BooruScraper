from Scraper.components.danbooru.components import ComponentsDanbooru
from Scraper.components.pixiv.components import ComponentPixiv
# from Scraper.components.yandere.components import ComponentYandere
# , "Yandere": ComponentYandere
from Scraper.components.pixiv_fast.components import ComponentPixivFast

AVAILABLE_MODULES = {"Pixiv": ComponentPixiv, "Pixiv Fast": ComponentPixivFast, "Danbooru": ComponentsDanbooru}
