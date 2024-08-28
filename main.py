import sys
import time
import dxcam
import mouse
import keyboard
from prepare_app import prepare_app
from constants import APPLICATION_TRIGGER, COLOR_TRIGGERS, PIXELS_PER_ITERATION, NEW_GAME_TRIGGER_POS

PAUSE_FLAG = False
PAUSE_KEY = 'k'
RESUME_KEY = 'l'
CHECK_INTERVAL = 0.1
DEFAULT_GAME_TIMEOUT = 5.5
MOUSE_MOVE_DELAY = 0.5
X_SHIFT = 20
Y_SHIFT_TOP = 150
Y_SHIFT_BOTTOM = 250

def toggle_pause():
    global PAUSE_FLAG
    PAUSE_FLAG = not PAUSE_FLAG
    state = "pausiert" if PAUSE_FLAG else "fortgesetzt"
    print(f"Autoclicker {state}...")

def is_game_running(frame, application_bbox):
    for x, y in APPLICATION_TRIGGER['positions']:
        x = int(x * (application_bbox[2] - application_bbox[0]) + application_bbox[0])
        y = int(y * (application_bbox[3] - application_bbox[1]) + application_bbox[1])
        if tuple(frame[y][x]) == tuple(APPLICATION_TRIGGER['color']):
            return True
    return False

def is_target_object(pixel):
    return (COLOR_TRIGGERS['red']['min'] <= pixel[0] <= COLOR_TRIGGERS['red']['max'] and
            COLOR_TRIGGERS['green']['min'] <= pixel[1] <= COLOR_TRIGGERS['green']['max'] and
            COLOR_TRIGGERS['blue']['min'] <= pixel[2] <= COLOR_TRIGGERS['blue']['max'])

def wait_for_game_to_start(camera, timeout=0.0):
    timer = time.time()
    application_bbox = prepare_app()
    while not is_game_running(camera.get_latest_frame(), application_bbox):
        application_bbox = prepare_app()
        if timeout > 0.0 and time.time() - timer > timeout:
            raise TimeoutError(f"Spiel wurde innerhalb von {timeout} Sekunden nicht gestartet.")

def play_game(camera, application_bbox, amount_of_games):
    game_counter = 0
    x_range = range(application_bbox[0] + X_SHIFT, application_bbox[2] - X_SHIFT, PIXELS_PER_ITERATION)
    y_range = range(application_bbox[1] + Y_SHIFT_TOP, application_bbox[3] - Y_SHIFT_BOTTOM, PIXELS_PER_ITERATION)

    while game_counter < amount_of_games:
        game_counter += 1
        print(f'Spiel {game_counter} gestartet.')
        frame = camera.get_latest_frame()

        while is_game_running(frame, application_bbox):
            if PAUSE_FLAG:
                time.sleep(CHECK_INTERVAL)
                continue

            for x in x_range:
                for y in y_range:
                    if is_target_object(frame[y][x]):
                        mouse.move(x, y, absolute=True)
                        mouse.click(button='left')
            frame = camera.get_latest_frame()

        print('Spiel beendet.')

        if game_counter < amount_of_games:
            start_new_game(application_bbox)
            wait_for_game_to_start(camera, timeout=DEFAULT_GAME_TIMEOUT)

def start_new_game(application_bbox):
    time.sleep(MOUSE_MOVE_DELAY)
    x = application_bbox[0] + int(NEW_GAME_TRIGGER_POS[0] * (application_bbox[2] - application_bbox[0]))
    y = application_bbox[1] + int(NEW_GAME_TRIGGER_POS[1] * (application_bbox[3] - application_bbox[1]))
    mouse.move(x, y, absolute=True)
    mouse.click(button='left')

def main():
    amount_of_games = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    camera = dxcam.create()
    camera.start(target_fps=60)

    print('Versuche, das laufende Spiel zu erkennen. Klicke auf "Spielen".')
    wait_for_game_to_start(camera)

    application_bbox = prepare_app()
    
    keyboard.add_hotkey(PAUSE_KEY, toggle_pause)
    keyboard.add_hotkey(RESUME_KEY, toggle_pause)

    play_game(camera, application_bbox, amount_of_games)

    camera.stop()

if __name__ == "__main__":
    main()
