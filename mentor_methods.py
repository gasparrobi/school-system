try:
    from .models import *
except Exception:
    from models import *





def get_list():
    table = Mentor.select()
    return table