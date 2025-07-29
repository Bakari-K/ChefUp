from django.db import migrations

def seed_tags(apps, schema_editor):
    Tag = apps.get_model('application', 'Tag')

    PREMADE_TAGS = [
        # Meal Type
        "breakfast", "lunch", "dinner", "brunch", "snack", "appetizer", "dessert",

        # Cuisine
        "italian", "mexican", "indian", "chinese", "thai", "japanese", "mediterranean",
        "french", "greek", "american",

        # Diet & Health
        "vegan", "vegetarian", "gluten-free", "dairy-free", "low-carb", "keto", "paleo", "high-protein",

        # Time & Difficulty
        "quick", "under-30-min", "easy", "intermediate", "advanced", "5-ingredients-or-less",

        # Occasion & Season
        "weeknight", "holiday", "summer", "winter", "party", "valentines", "thanksgiving", "christmas",

        # Cooking Method
        "grilled", "baked", "fried", "slow-cooked", "air-fryer", "no-cook", "instant-pot"
    ]

    for name in PREMADE_TAGS:
        Tag.objects.get_or_create(name=name)

def unseed_tags(apps, schema_editor):
    Tag = apps.get_model('application', 'Tag')

    PREMADE_TAGS = [
        "breakfast", "lunch", "dinner", "brunch", "snack", "appetizer", "dessert",
        "italian", "mexican", "indian", "chinese", "thai", "japanese", "mediterranean",
        "french", "greek", "american",
        "vegan", "vegetarian", "gluten-free", "dairy-free", "low-carb", "keto", "paleo", "high-protein",
        "quick", "under-30-min", "easy", "intermediate", "advanced", "5-ingredients-or-less",
        "weeknight", "holiday", "summer", "winter", "party", "valentines", "thanksgiving", "christmas",
        "grilled", "baked", "fried", "slow-cooked", "air-fryer", "no-cook", "instant-pot"
    ]

    Tag.objects.filter(name__in=PREMADE_TAGS).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_tags, reverse_code=unseed_tags),
    ]
