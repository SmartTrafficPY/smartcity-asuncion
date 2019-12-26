from django.apps import AppConfig


class UccarpoolConfig(AppConfig):
    name = "uccarpool"

    time_tolerance_early_in_minutes = 15
    time_tolerance_late_in_minutes = 10

    common_instituion = "Universidad Catolica"
    institution_location = {"latitude": -25.324488, "longitude": -57.635435}
    min_walking_distance = 500  # In meters

    personality_weights_proportion = 0.15  # 15%

    """
    All weights added must be a total of 1.0
    """
    personality_heuristic_weights = {
        "smoke": 0.358725,
        "eloquence_level": 0.265280,
        "musicTaste": 0.218275,
        "sex": 0.15772,
    }

    logistic_heuristic_weights = {
        "distance_to_destination": 0.85,
        "walking_distance_to_path": 0.15,
    }
