#!/usr/bin/python3

import hlt
import logging

game = hlt.Game("Gundam")
logging.info("Starting my Settler bot!")

while True:
    game_map = game.update_map()
    command_queue = []

    my_ships = game_map.get_me().all_ships()
    for ship in my_ships:

        docked = ship.docking_status != ship.DockingStatus.UNDOCKED
        if docked:
            continue

        all_planets = game_map.all_planets()
        for planet in all_planets:
            owned = planet.is_owned()

            if owned:
                continue

            number_docked_ships = len(planet.all_docked_ships())
            if ship.can_dock(planet) and number_docked_ships < 3:
                command_queue.append(ship.dock(planet))
            else:
                navigate_command = ship.navigate(ship.closest_point_to(planet), game_map, speed=hlt.constants.MAX_SPEED, ignore_ships=True)
                if navigate_command:
                    command_queue.append(navigate_command)
            break

    game.send_command_queue(command_queue)

