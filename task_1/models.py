from django.db import models
from django.utils import timezone


class Player(models.Model):
    
    username = models.CharField(max_length=50)
    boosts = models.IntegerField(default=0)
    first_login = models.DateTimeField()
    daily_login_points = models.IntegerField(default=0)
    
    def login(self, quantity):
        """Метод для обработки входа игрока и начисления баллов."""
        if not self.first_login:
            self.first_login = timezone.now()
        self.boosts += quantity
        self.save()
    
    def award_boost(self, boost_type, amount):
        """Начислить игроку буст."""
        Boost.objects.create(player=self, type=boost_type, amount=amount)
        self.boosts += 1
        self.save()


class Boost(models.Model):
    BOOST_TYPES = (
        ('speed', 'Speed Boost'),
        ('strength', 'Strength Boost'),
        ('defense', 'Defense Boost'),
    )
    
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='boost',
    )
    type = models.CharField(max_length=50, choices=BOOST_TYPES)
    boost = models.IntegerField(default=0)
    awarded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.type} Boost for {self.player.username}: {self.boost}'
    