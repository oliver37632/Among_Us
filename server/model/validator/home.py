from schematics.models import Model
from schematics.types import DateType


class PostValidator(Model):
    title = DateType(serialized_name="title", required=True, min_length=1, max_length=20)
    content = DateType(serialized_name="content", required=True, min_length=1, max_length=1000)
    town = DateType(serialized_name="town", required=True, min_length=1, max_length=45)
    category = DateType(serialized_name="category", required=True, min_length=10, max_length=45)
    price = DateType(serialized_name="price", required=True, min_length=1, max_length=100)
    image = DateType(serialized_name="image", required=True)
