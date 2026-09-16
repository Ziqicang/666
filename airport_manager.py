
airport_info = ("OUL", 1, "14-09-2026")
allowed_gates = {"A1", "A2", "A3", "A4", "B1", "B2"}
restricted_destinations = {"Moscow", "Pyongyang"}

flights = {
    "AY450": {
        "destination": "Helsinki",
        "departure": "08:30",
        "gate": "A2",
        "capacity": 5,
        "passengers": ["Alice Wong", "David Kim", "Fatima Ali"]
    },
    "SK271": {
        "destination": "Stockholm",
        "departure": "10:15",
        "gate": "B1",
        "capacity": 4,
        "passengers": ["Chen Wei", "George Smith"]
    },
    "LH2491": {
        "destination": "Munich",
        "departure": "12:40",
        "gate": "A4",
        "capacity": 5,
        "passengers": ["Hana Lee", "Maria Garcia", "Noah Wilson"]
    }
}


def find_flight(flights, flight_number):
    if not flight_number or not isinstance(flight_number, str):
        return None
    target = flight_number.strip().upper()
    for key in flights:
        if key.strip().upper() == target:
            return key
    return None


def passenger_exists(passengers, passenger_name):
    if not passenger_name or not isinstance(passenger_name, str):
        return False
    target = passenger_name.strip().lower()
    for p in passengers:
        if p.strip().lower() == target:
            return True
    return False


def check_in_passenger(flights, flight_number, passenger_name, restricted_destinations):
    if not passenger_name or not passenger_name.strip():
        return "EMPTY_NAME"

    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    flight = flights[flight_key]

    dest = flight.get("destination", "")
    restricted_lower = {d.strip().lower() for d in restricted_destinations if isinstance(d, str)}
    if dest.strip().lower() in restricted_lower:
        return "RESTRICTED"

    if len(flight["passengers"]) >= flight["capacity"]:
        return "FULL"

    if passenger_exists(flight["passengers"], passenger_name):
        return "DUPLICATE"

   
    flight["passengers"].append(passenger_name.strip().title())
    return "OK"


def remove_passenger(flights, flight_number, passenger_name):
    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    flight = flights[flight_key]
    target = passenger_name.strip().lower() if passenger_name else ""

    for i, p in enumerate(flight["passengers"]):
        if p.strip().lower() == target:
            flight["passengers"].pop(i)
            return "OK"

    return "PASSENGER_NOT_FOUND"


def change_gate(flights, flight_number, new_gate, allowed_gates):
    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    cleaned_gate = new_gate.strip().upper() if new_gate else ""
    allowed_upper = {g.strip().upper() for g in allowed_gates if isinstance(g, str)}

    if cleaned_gate not in allowed_upper:
        return "INVALID_GATE"

    matching_gate = cleaned_gate
    for g in allowed_gates:
        if g.strip().upper() == cleaned_gate:
            matching_gate = g
            break

    flights[flight_key]["gate"] = matching_gate
    return "OK"


def flight_status(flight):
    capacity = flight.get("capacity", 0)
    count = len(flight.get("passengers", []))
    percentage = (count / capacity) * 100 if capacity > 0 else 0.0

    if percentage == 100:
        return "FULL"
    elif percentage >= 75:
        return "ALMOST FULL"
    else:
        return "AVAILABLE"


def sorted_manifest(flights, flight_number):
    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return None

    return sorted(flights[flight_key]["passengers"])


def total_passengers(flights):
    return sum(len(flight["passengers"]) for flight in flights.values())


def any_full_flight(flights):
    for flight in flights.values():
        if len(flight["passengers"]) >= flight["capacity"]:
            return True
    return False


def all_flights_have_passengers(flights):
    if not flights:
        return False
    for flight in flights.values():
        if len(flight["passengers"]) == 0:
            return False
    return True