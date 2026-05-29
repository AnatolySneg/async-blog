# By importing models here, we ensure that Alembic sees them all at once,
# just by importing `from src.models import Base` in the env.py file.

from .base import Base

from .user import User
# from .tag import Tag, post_tags
from .post import Post

# Optional: explicitly specify what is exported from the package
# __all__ = ["Base", "User", "Post", "Tag", "post_tags"]
__all__ = ["Base", "User", "Post"]
