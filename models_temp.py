class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=3000, null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    viewers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='viewed_posts',
        editable=False
    )
    search_vector = SearchVectorField(null=True, editable=False)
    objects = PostManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Post.objects.update(search_vector = (   SearchVector('title', weight='A', config='english') +
                                                SearchVector('content', weight='B', config='english'))
                                            )

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
