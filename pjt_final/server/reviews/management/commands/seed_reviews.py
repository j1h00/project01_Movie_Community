from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.auth import get_user_model
from ...models import Review, Movie
import random

class Command(BaseCommand):
    help = "이 커맨드를 통해 랜덤한 리뷰 데이터를 만듭니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            default=200,
            type=int,
            help="리뷰 생성 개수를 지정"
    )
    
    def handle(self, *args, **options):
        total = options.get("total")
        seeder = Seed.seeder()

        users = get_user_model().objects.all() 
        movies = Movie.objects.all() 
        seeder.add_entity( Review, total, { 
            'user': lambda x: random.choice(users), 
            'movie': lambda x: random.choice(movies),
            'rating': lambda x: random.choice(list(range(1, 11))),
            'content': lambda x: seeder.faker.text(),
            })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{total}개의 리뷰가 작성되었습니다."))