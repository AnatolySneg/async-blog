import enum


class UserRole(str, enum.Enum):
    user="user"
    moderator="moderator"
    banned="banned"
    deleted="deleted"


class PostStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    deleted = "deleted"
