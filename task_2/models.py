from datetime import date

from django.db import models


class Player(models.Model):
    player_id = models.CharField(max_length=100)


class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)


class Prize(models.Model):
    title = models.CharField(max_length=100)


class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField()
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)
    
    def assign_prize(self):
        level_prize = LevelPrize.objects.get(level=self.level)
        prize = level_prize.prize
        
        if self.is_completed:
            PlayerPrize.objects.create(
                player=self.player,
                prize=prize,
                received=date.today(),
            )
            

class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()


class PlayerPrize(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateTimeField()