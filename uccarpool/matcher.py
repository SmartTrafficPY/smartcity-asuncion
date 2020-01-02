from datetime import timedelta

from django.apps import apps
from django.db.models import Q
from rest_framework.exceptions import APIException
from smrouter.utils import Router
from uccarpool import heuristic_functions
from uccarpool.models import Carpool, ItineraryRoute, UserItinerary


class UserAlreadyInCarpool(APIException):
    status_code = 420
    default_detail = "The user is already in a carpool."
    default_code = "service_unavailable"


def calculateLogisticMatch(meeting_point, route):
    """Calculates the logistics aspect of the carpooling math formula"""

    logistics_affinity = 0.0

    logistic_heuristic_weights = apps.get_app_config("uccarpool").logistic_heuristic_weights
    logistic_weights_proportion = 1 - apps.get_app_config("uccarpool").personality_weights_proportion

    # calcula el porcentaje de caminata comparado a la distancia maxima de caminata configurada para la app
    min_walking_distance = apps.get_app_config("uccarpool").min_walking_distance

    logistics_affinity = logistic_heuristic_weights["walking_distance_to_path"] * (
        (min_walking_distance - meeting_point["cost"]) / min_walking_distance
    )

    # Calcula el porcentaje de distancia recorrida
    index = route.path.index(meeting_point["end_vid"])
    route_cost = route.aggCost[-1]
    cost_meeting_point = route.aggCost[index]

    logistics_affinity += logistic_heuristic_weights["distance_to_destination"] * (
        (route_cost - cost_meeting_point) / route_cost
    )

    return logistic_weights_proportion * logistics_affinity


def calculatePersonalityMatch(UserA, UserB):
    """Calculates affinity between A and B in respect of personality traits"""

    personality_affinity = 0.0

    heuristic_weights = apps.get_app_config("uccarpool").personality_heuristic_weights
    personality_weights_proportion = apps.get_app_config("uccarpool").personality_weights_proportion

    personality_affinity = (
        heuristic_weights["smoke"] * heuristic_functions.function_smoker(UserA.smoker, UserB.smoker)
        + heuristic_weights["eloquence_level"]
        * heuristic_functions.function_eloquence_level(UserA.eloquenceLevel, UserB.eloquenceLevel)
        + heuristic_weights["musicTaste"]
        * heuristic_functions.function_music_taste(UserA.musicTaste, UserB.musicTaste)
        + heuristic_weights["sex"] * heuristic_functions.function_sex(UserA.sex, UserB.sex)
    )

    return personality_affinity * personality_weights_proportion


def getRouteItinerary(itinerary):
    """Aqui obtiene la ruta para el itinerario y la guarda un una BD"""

    # obtener la ruta de la BD
    router = Router()
    path = router.driver_path(origin=itinerary.origin, destination=itinerary.destination)

    # Convertir a array y guardar en el modelo ItineraryRoute
    ItineraryRoute.objects.create(itinerary=itinerary, path=path)

    return path


def isInCarpool(userUcarpoolingProfile, userItinerary):
    """Returns true if the user is already in a carpool with that itinerary"""
    carpools = Carpool.objects.all().filter(Q(driver=userUcarpoolingProfile) | Q(poolers=userUcarpoolingProfile))
    if carpools:
        return True
    else:
        return False


def getMatchedUsers(userUcarpoolingProfile, userItinerary):
    """Procedure that returns the list of users who have a % match greater than 0 with user"""

    if isInCarpool(userUcarpoolingProfile, userItinerary):
        raise UserAlreadyInCarpool

    """Se obtienen los itinerarios compatibles con +- 15 minutos de diferencia para llegar al destino"""
    date_start = userItinerary.timeOfArrival - timedelta(
        minutes=apps.get_app_config("uccarpool").time_tolerance_early_in_minutes
    )
    date_finish = userItinerary.timeOfArrival + timedelta(
        minutes=apps.get_app_config("uccarpool").time_tolerance_late_in_minutes
    )
    compatible_itineraries = UserItinerary.objects.filter(timeOfArrival__range=(date_start, date_finish)).exclude(
        ucarpoolingProfile=userUcarpoolingProfile
    )

    """Si hubieron personas compatibles con su horario"""
    matched_users = []
    if compatible_itineraries:

        if userItinerary.isDriver:
            userItineraryRoute = ItineraryRoute.objects.get(itinerary=userItinerary)

        """Para cada itinerario compatible"""
        for another_user_itinerary in compatible_itineraries:

            """-----Filtro de Pre compatibilidad------"""

            """Another user is already in a carpool"""
            if isInCarpool(another_user_itinerary.ucarpoolingProfile, another_user_itinerary):
                continue

            """Si las 2 personas son passengers entonces son incompatibles"""
            if userItinerary.isDriver is False and another_user_itinerary.isDriver is False:
                continue

            """
            Chequear si son compatibles en la trayectoria,
            es decir, si el origen de alguno queda a menos de X metros del trayecto del otro.
            """
            router = Router()
            min_walking_distance = apps.get_app_config("uccarpool").min_walking_distance

            puede_ser_buscado = False
            puede_buscar = False

            """Si el otro es chofer, quien pasa por el camino"""
            if another_user_itinerary.isDriver:

                # Obtener la trayectoria del otro usuario
                another_user_itinerary_route = ItineraryRoute.objects.get(itinerary=another_user_itinerary)

                # Comparar el origen del usuario contra la ruta del otro usuario
                min_distance_point_to_path = router.get_min_distance(
                    point=userItinerary.origin, path=another_user_itinerary_route.path
                )

                # Controlar que si alguna de la distancia minima es menos que X metros
                if min_distance_point_to_path["cost"] < min_walking_distance:
                    puede_ser_buscado = True  # el usuario puede ser buscado por el otro usuario

            """Si el usuario es chofer, chequear si su trayecto pasa por la casa del otro usuario"""
            if userItinerary.isDriver:

                min_distance_path_to_origin = router.get_min_distance(
                    point=another_user_itinerary.origin, path=userItineraryRoute.path
                )

                # Controlar que si alguna de la distancia minima es menos que X metros
                if min_distance_path_to_origin["cost"] < min_walking_distance:
                    puede_buscar = True  # el usuario puede ser buscar por el otro usuario

            if (not puede_ser_buscado) and (not puede_buscar):
                # Si no puede buscar ni puede ser buscado
                continue

            """
            -----
            Son pre-compatibles y pueden hacer carpool juntos.
            Ahora se calcula el porcentaje de afinidad entre los 2
            ------
            """

            # Calculo de procentaje de compatibilidad heuristica #

            # Calcular/get el procentaje de compatibilidad de personalidades 2.2.1-2.2.4

            personality_match_percentage = calculatePersonalityMatch(
                userItinerary.ucarpoolingProfile, another_user_itinerary.ucarpoolingProfile
            )

            # Calcular el porcentaje de compatibilidad de distancias 2.2.5 y 2.2.6

            if puede_ser_buscado:
                """Calculate the match percentage if the user is to be picked up by another user"""
                puede_ser_buscado_match_percentage = personality_match_percentage + calculateLogisticMatch(
                    min_distance_point_to_path, another_user_itinerary_route
                )

            if puede_buscar:
                """Calculate the match percentage if the user picks up another user"""
                puede_buscar_match_percentage = personality_match_percentage + calculateLogisticMatch(
                    min_distance_path_to_origin, userItineraryRoute
                )

            matched_user = {
                "user_id": another_user_itinerary.ucarpoolingProfile.id,
                "user": another_user_itinerary.ucarpoolingProfile.user.username,
            }

            if puede_ser_buscado and puede_buscar:
                if puede_ser_buscado_match_percentage > puede_buscar_match_percentage:
                    """Is better to be picked up by another user"""
                    matched_user["role"] = "ser buscado"
                    matched_user["match_percentage"] = puede_ser_buscado_match_percentage
                    matched_user["meeting_point"] = min_distance_point_to_path["end_vid"]
                else:
                    """Is better to be pick up another user"""
                    matched_user["role"] = "buscar"
                    matched_user["match_percentage"] = puede_buscar_match_percentage
                    matched_user["meeting_point"] = min_distance_path_to_origin["end_vid"]
            elif puede_ser_buscado:
                matched_user["role"] = "ser buscado"
                matched_user["match_percentage"] = puede_ser_buscado_match_percentage
                matched_user["meeting_point"] = min_distance_point_to_path["end_vid"]
            else:
                matched_user["role"] = "buscar"
                matched_user["match_percentage"] = puede_buscar_match_percentage
                matched_user["meeting_point"] = min_distance_path_to_origin["end_vid"]

            matched_users.append(matched_user)

    return matched_users
