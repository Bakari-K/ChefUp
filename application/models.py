from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    is_public = models.BooleanField(default=True)

# Many Images to one Recipe
class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='recipe_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Many Reviews to One Recipe
class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Guarantees one review per user
    class Meta:
        unique_together = ('recipe', 'user')

# Only one status tag for each recipe and user combination
class RecipeStatusTag(models.Model):
    STATUS_CHOICES = [
        ('want_to_make', 'Want to Make'),
        ('making', 'Currently Making'),
        ('made', 'Made'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe', 'status')

# Many comments for reach recipe and user
class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Each recipe can have many tags
# Still unsure whether we should set each tag or whether users can make them
# If we set them then we should replace this with a constant set.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
