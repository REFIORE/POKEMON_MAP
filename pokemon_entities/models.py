from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(verbose_name='Название на русском', max_length=200)
    title_en = models.CharField(verbose_name='Название на англоийском', max_length=200)
    title_jp = models.CharField(verbose_name='Название на японском', max_length=200)
    image = models.ImageField(verbose_name='Изображение', null=True, upload_to="images", default="image")
    description = models.TextField(verbose_name='Описание покемона', blank=True)
    previous_evolution = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='next_evolution', verbose_name='Предыдущая эволюция')
    id = models.BigAutoField(verbose_name='ID покемона', primary_key=True)

    def __str__(self):
        return '{}'.format(self.title)


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Дата и время появления покемона', null=True)
    disappeared_at = models.DateTimeField(verbose_name='Дата и время исчезновения покемона', null=True)
    level = models.IntegerField(verbose_name='Уровень', blank=True, null=True)
    health = models.IntegerField(verbose_name='Здоровье', blank=True, null=True)
    strength = models.IntegerField(verbose_name='Атака', blank=True, null=True)
    defence = models.IntegerField(verbose_name='Защита', blank=True, null=True)
    stamina = models.IntegerField(verbose_name='Выносливость', blank=True, null=True)
