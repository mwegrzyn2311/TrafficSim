class SimmStats:
    car_id = 0
    turn = 0
    stats_per_turn = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SimmStats, cls).__new__(cls)
        return cls.instance

    def register_num_of_drivers(self, drivers_no):
        self.stats_per_turn[self.turn]["drivers"]["total"] = drivers_no

    def register_cars_per_road(self, road, cars_in_road):
        self.stats_per_turn[self.turn]["city"]["roads"][
            f"({road.left_node.pos.x},{road.left_node.pos.y}) -> ({road.right_node.pos.x},{road.right_node.pos.y})"] = cars_in_road

    def register_cars_per_gateway(self, gateway, cars_in_gateway_queue):
        self.stats_per_turn[self.turn]["city"]["gateways"][f"({gateway.pos.x},{gateway.pos.y})"] = cars_in_gateway_queue

    def register_total_cars_in_city(self, cars_in_city):
        self.stats_per_turn[self.turn]["city"]["total"] = cars_in_city

    def register_speed(self, min_spd, max_spd, avg_spd):
        self.stats_per_turn[self.turn]["speed"]["min"] = min_spd
        self.stats_per_turn[self.turn]["speed"]["max"] = max_spd
        self.stats_per_turn[self.turn]["speed"]["avg"] = avg_spd

    def next_turn(self):
        self.turn += 1
        self.stats_per_turn[self.turn] = {
            "drivers": {},
            "city": {
                "roads": {},
                "gateways": {},
            },
            "speed": {}
        }

    def get_next_car_id(self):
        self.car_id += 1
        return self.car_id
