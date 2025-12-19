from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


# ================= CATEGORY =================
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ================= POST =================
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    # URL based image (no local / no cloud storage required)
    img_url = models.URLField(
        blank=True,
        null=True,
        default="https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Safe slug generator
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

   


# ================= ABOUT US =================
class Aboutus(models.Model):
    content = models.TextField()








