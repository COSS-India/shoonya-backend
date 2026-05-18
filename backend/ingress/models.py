from django.db import models


# Create your models here.

def crawler_directory_path(instance, filename):
    # This will dynamically upload the file to: MEDIA_ROOT/crawlers/{instance.name}/%Y/%m/%d/{filename}
    return f'crawlers/{instance.name}/%Y/%m/%d/{filename}'


class Crawler(models.Model):
    """
    Crawler Model
    """

    name = models.CharField(
        max_length=255,
        editable=False,  # So that upload path does not change as it is being used to upload script file
    )
    root_url = models.URLField()
    script = models.FileField(
        upload_to=crawler_directory_path
    )
    configuration = models.JSONField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'crawlers'
        verbose_name = 'Crawler'
        verbose_name_plural = 'Crawlers'
        ordering = ('name',)


class CrawledRun(models.Model):
    crawler = models.ForeignKey(
        "ingress.Crawler",
        on_delete=models.CASCADE,
        related_name='crawled_runs',
    )
    metadata = models.JSONField()

    def __str__(self):
        return f'{self.crawler.name}::{self.pk}'

    class Meta:
        db_table = 'crawled_runs'
        verbose_name = 'Crawled Run'
        verbose_name_plural = 'Crawled Runs'
