from datetime import timedelta

from django.apps import apps
from smrouter.utils import Router
from uccarpool import heuristic_functions
from uccarpool.models import ItineraryRoute, UserItinerary


def calculateLogisticMatch():
    """ """
    # TODO
    return 50.0


def calculatePersonalityMatch(UserA, UserB):
    """Calculates affinity between A and B in respect of personality traits"""

    personality_affinity = 0.0

    heuristic_weights = apps.get_app_config("personality_heuristic_weights")
    personality_weights_proportion = apps.get_app_config("personality_weights_proportion")

    personality_affinity = (
        heuristic_weights["smoke"] * heuristic_functions.function_smoker(UserA.smoker, UserB.smoker)
        + heuristic_weights["eloquence_level"]
        * heuristic_functions.function_sex(UserA.eloquence_level, UserB.eloquence_level)
        + heuristic_weights["musicTaste"] * heuristic_functions.function_sex(UserA.musicTaste, UserB.musicTaste)
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


def getMatchedUsers(userUcarpoolingProfile, userItinerary):
    """Procedure that returns the list of users who have a % match greater than 0 with user"""

    """Si es chofer, guarda la trayectoria al destino para calculos posteriores"""
    if userItinerary.isDriver:
        route = getRouteItinerary(userItinerary)

    """Se obtienen los itinerarios compatibles con +- 15 minutos de diferencia para llegar al destino"""
    date_start = userItinerary.timeOfArrival - timedelta(hours=0, minutes=15)
    date_finish = userItinerary.timeOfArrival + timedelta(hours=0, minutes=15)
    compatible_itineraries = UserItinerary.objects.filter(timeOfArrival__range=(date_start, date_finish)).exclude(
        ucarpoolingProfile=userUcarpoolingProfile
    )

    """Si hubieron personas compatibles con su horario"""
    if compatible_itineraries:

        matched_users = []

        """Para cada itinerario compatible"""
        for another_user_itinerary in compatible_itineraries:

            """-----Filtro de Pre compatibilidad------"""

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
                another_user_itinerary_path = ItineraryRoute.objects.get(itinerary=another_user_itinerary).path

                # Comparar el origen del usuario contra la ruta del otro usuario
                min_distance_point_to_path = router.get_min_distance(
                    point=userItinerary.origin, path=another_user_itinerary_path
                )

                # Controlar que si alguna de la distancia minima es menos que X metros
                if min_distance_point_to_path < min_walking_distance:
                    puede_ser_buscado = True  # el usuario puede ser buscado por el otro usuario

            """Si el usuario es chofer, chequear si su trayecto pasa por la casa del otro usuario"""
            if userItinerary.isDriver:

                min_distance_path_to_origin = router.get_min_distance(point=another_user_itinerary.origin, path=route)

                # Controlar que si alguna de la distancia minima es menos que X metros
                if min_distance_path_to_origin < min_walking_distance:
                    puede_buscar = True  # el usuario puede ser buscar por el otro usuario

            if (not puede_ser_buscado) and (not puede_buscar):
                # Si no puede buscar ni puede ser buscado
                continue

            # Verificar si el carpool esta lleno

            """
            -----
            Son pre-compatibles y pueden hacer carpool juntos.
            Ahora se calcula el porcentaje de afinidad entre los 2
            ------
            """

            # Calculo de procentaje de compatibilidad heuristica #

            # Calcular/get el procentaje de compatibilidad de personalidades 2.2.1-2.2.4

            match_percentage = calculatePersonalityMatch(
                userItinerary.ucarpoolingProfile, another_user_itinerary.ucarpoolingProfile
            )

            # Calcular el porcentaje de compatibilidad de distancias 2.2.5 y 2.2.6
            # TODO
            match_percentage += calculateLogisticMatch()

    if not matched_users:
        return "Didn't find compatible itineraries"
    else:
        return matched_users
