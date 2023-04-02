import keyboard
import json

last_keys = []
current_modifiers = []


def main():
    with open('translit_defs.json', encoding="utf8") as json_file:
        translit_dict = json.load(json_file)

    while True:
        event = keyboard.read_event(suppress=True)
        if event.event_type == "down":
            if ("ctrl" in event.name or "alt" in event.name or "windows" in event.name) and event.name not in current_modifiers:
                current_modifiers.append(event.name)

            if event.name == "right alt":
                bypass = True

            if len(current_modifiers) > 0:
                keyboard.press(event.name)
                continue

            if len(last_keys) > 0 and last_keys[-1].lower() + event.name.lower() in translit_dict:
                keyboard.press_and_release("backspace")
                if event.name.isupper() or last_keys[-1].isupper():
                    keyboard.write(
                        translit_dict[last_keys[-1].lower() + event.name.lower()].upper())

                else:
                    keyboard.write(
                        translit_dict[last_keys[-1].lower() + event.name.lower()])

            elif event.name.lower() in translit_dict:
                if event.name.isupper():
                    keyboard.write(translit_dict[event.name.lower()].upper())

                else:
                    keyboard.write(translit_dict[event.name.lower()])

            else:
                keyboard.press(event.name)

            if len(last_keys) == (max(map(len, translit_dict))):
                for i in range(max(map(len, translit_dict)) - 1):
                    last_keys.remove(last_keys[i])

            if all(x not in event.name.lower() for x in ["ctrl", "alt", "windows", "shift"]):
                last_keys.append(event.name)

        elif event.event_type == "up":
            if "ctrl" in event.name or "alt" in event.name or "windows" in event.name:
                current_modifiers.remove(event.name)

            if len(current_modifiers) > 0:
                keyboard.release(event.name)
                continue

            if event.name not in translit_dict:
                keyboard.release(event.name)


if __name__ == "__main__":
    main()
