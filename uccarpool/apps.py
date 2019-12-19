from django.apps import AppConfig


class UccarpoolConfig(AppConfig):
    name = "uccarpool"

    common_instituion = "Universidad Catolica"
    institution_location = {"latitude": -25.324488, "longitude": -57.635435}
    min_walking_distance = 400  # In meters

    personality_weights_proportion = 0.20  # 20%

    """
    All weights added must be a total of 1.0
    """
    personality_heuristic_weights = {
        "smoking": 0.358725,
        "eloquence_level": 0.265280,
        "musicTaste": 0.218275,
        "sex": 0.15772,
    }

    logistic_heuristic_weights = {
        "distance_to_origin": 0.8,
        "distance_to_path": 0.2,
    }
