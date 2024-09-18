import csv
from django.http import HttpResponse

from task_2.models import PlayerLevel


def export_player_level_prizes_to_csv():
    response = HttpResponse(content_type='text/csv')
    response[
        'Content-Disposition'] = 'attachment; filename="player_level_prizes.csv"'
    
    writer = csv.writer(response)

    writer.writerow(['Player ID', 'Level Title', 'Is Completed', 'Prize Title'])

    queryset = PlayerLevel.objects.select_related('player',
                                                  'level').prefetch_related(
        'level__levelprize_set__prize')
    for player_level in queryset.iterator(chunk_size=1000):
        prizes = player_level.level.levelprize_set.all()
        for prize in prizes:
            writer.writerow([
                player_level.player.player_id,
                player_level.level.title,
                player_level.is_completed,
                prize.prize.title
            ])
    
    return response
