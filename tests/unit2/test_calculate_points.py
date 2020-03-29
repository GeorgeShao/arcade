import arcadeplus

def test_calculate_points():
    texture = arcadeplus.load_texture(":resources:images/items/coinGold.png")
    result = arcadeplus.calculate_points(texture.image)
    print(result)

    texture = arcadeplus.load_texture(":resources:images/animated_characters/female_person/femalePerson_idle.png")
    result = arcadeplus.calculate_points(texture.image)
    print(result)
