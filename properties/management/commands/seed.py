from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from properties.models import Property, UserProfile


class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **options):
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            UserProfile.objects.get_or_create(user=admin)
            self.stdout.write('Admin user created: admin/admin123')

        # Create demo user
        if not User.objects.filter(username='demo').exists():
            demo = User.objects.create_user('demo', 'demo@example.com', 'demo123',
                                             first_name='Demo', last_name='Paydalanıwshı')
            UserProfile.objects.get_or_create(user=demo)
        else:
            demo = User.objects.get(username='demo')

        sample_properties = [
            {
                'title': 'Nókiste 3 bólmeli páter',
                'description': 'Nókis qalasınıń oraylıq bóliminde jaylasqan, jańa remontlı 3 bólmeli páter. Barlıq kommunikaciyalar bar.',
                'listing_type': 'sale',
                'property_type': 'apartment',
                'price': 45000,
                'city': 'Nókis',
                'address': 'Doslik kóshesi, 12-úy',
                'area': 75,
                'rooms': 3,
                'bathrooms': 1,
                'floor': 4,
                'total_floors': 9,
                'year_built': 2018,
                'condition': 'good',
                'phone': '+998 61 222 3344',
                'is_featured': True,
            },
            {
                'title': 'Nókiste jańa 2 bólmeli páter ijara',
                'description': 'Qalada qulay jaylasqan, mebelli, internet bár páter. Úzaq múddetli ijara ushın.',
                'listing_type': 'rent',
                'property_type': 'apartment',
                'price': 300,
                'city': 'Nókis',
                'address': 'Ámiwdárya kóshesi, 5-úy',
                'area': 55,
                'rooms': 2,
                'bathrooms': 1,
                'floor': 2,
                'total_floors': 5,
                'year_built': 2015,
                'condition': 'good',
                'phone': '+998 61 222 5566',
                'is_featured': True,
            },
            {
                'title': 'Beruniy qalasında úy satıladı',
                'description': 'Keng jaylaǵan, aywanı bar, baqsha jerleri menen birge jeke úy.',
                'listing_type': 'sale',
                'property_type': 'house',
                'price': 65000,
                'city': 'Beruniy',
                'address': 'Nawrız kóshesi, 33-úy',
                'area': 180,
                'rooms': 5,
                'bathrooms': 2,
                'floor': 1,
                'total_floors': 2,
                'year_built': 2010,
                'condition': 'good',
                'phone': '+998 61 333 7788',
                'is_featured': False,
            },
            {
                'title': 'Xójeli qalasında kommerciyalıq jay',
                'description': 'Oraylıq kóshede jaylasqan, dúkan yaki ofis ushın qolaylı jay.',
                'listing_type': 'rent',
                'property_type': 'commercial',
                'price': 500,
                'city': 'Xójeli',
                'address': 'Bazar kóshesi, 1-úy',
                'area': 80,
                'rooms': 2,
                'bathrooms': 1,
                'condition': 'good',
                'phone': '+998 61 444 9900',
                'is_featured': False,
            },
            {
                'title': 'Qońırat qalasında jer maydanı',
                'description': 'Qońırat qalasınıń shegarasında qurlıs ushın tayın jer. Barıq dokumentler tárt̃ibinde.',
                'listing_type': 'sale',
                'property_type': 'land',
                'price': 12000,
                'city': 'Qońırat',
                'address': 'Suwlı kóshesi boyı',
                'area': 600,
                'rooms': 0,
                'bathrooms': 0,
                'condition': 'new',
                'phone': '+998 61 555 1122',
                'is_featured': True,
            },
            {
                'title': 'Nókiste 1 bólmeli kvartura ijara',
                'description': 'Jeke kishi páter, talabınıza qaray mebelli yaki mebelisiz beriledi.',
                'listing_type': 'rent',
                'property_type': 'apartment',
                'price': 150,
                'city': 'Nókis',
                'address': 'Mustaqillik kóshesi, 7-úy',
                'area': 35,
                'rooms': 1,
                'bathrooms': 1,
                'floor': 3,
                'total_floors': 5,
                'year_built': 2005,
                'condition': 'good',
                'phone': '+998 61 666 3344',
                'is_featured': False,
            },
        ]

        for data in sample_properties:
            if not Property.objects.filter(title=data['title']).exists():
                Property.objects.create(owner=demo, **data)

        self.stdout.write(self.style.SUCCESS(f'Seed data created successfully! {len(sample_properties)} properties added.'))
