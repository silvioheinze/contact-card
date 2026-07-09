from django.db import models


class Card(models.Model):
    user = models.OneToOneField(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='card',
    )
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__slug']

    def __str__(self):
        return self.display_name or self.user.slug

    @property
    def display_name(self):
        name = f'{self.first_name} {self.last_name}'.strip()
        return name

    @property
    def slug(self):
        return self.user.slug

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('cards:detail', kwargs={'slug': self.slug})


class CardLink(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='links')
    label = models.CharField(max_length=100)
    url = models.URLField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f'{self.label}: {self.url}'
