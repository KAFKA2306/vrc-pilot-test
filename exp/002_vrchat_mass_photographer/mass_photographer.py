import time
from pathlib import Path

import vrcpilot


def find_and_click(text_query, pid, screenshot_name="debug.png", timeout=10):
    print(f"Searching for '{text_query}'...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        img = vrcpilot.take_screenshot(pid=pid)
        img.save(Path(screenshot_name))
        result = vrcpilot.ocr(img)
        for word in result.words:
            if text_query.lower() in word.text.lower():
                x, y, w, h = word.bbox
                cx, cy = int(x + w / 2), int(y + h / 2)
                print(f"Found '{word.text}' at ({cx}, {cy}). Clicking...")
                vrcpilot.mouse.move(cx, cy, pid=pid)
                vrcpilot.mouse.click(vrcpilot.MouseButton.LEFT, pid=pid)
                return True
        time.sleep(1)
    return False


def take_photos(pid, world_index, num_photos=3):
    print(f"Taking {num_photos} photos in World {world_index}...")
    for i in range(num_photos):
        filename = f"world_{world_index}_photo_{i+1}.png"
        img = vrcpilot.take_screenshot(pid=pid)
        img.save(Path(filename))
        print(f"Saved {filename}")
        print("Rotating camera...")
        vrcpilot.keyboard.press(vrcpilot.Key.D, duration=0.5, pid=pid)
        time.sleep(1)


def main():
    print("--- VRChat Mass Photographer Agent ---")
    pid = vrcpilot.launch(
        no_vr=True,
        screen_width=1280,
        screen_height=720,
        wait_timeout=60,
    )
    print(f"VRChat launched. PID: {pid}")

    print("Waiting for initialization (45s)...")
    time.sleep(45)

    vrcpilot.focus(pid=pid)

    for world_idx in range(1, 4):
        print(f"\n--- Visiting World {world_idx} ---")

        vrcpilot.keyboard.press(vrcpilot.Key.ESCAPE, pid=pid)
        time.sleep(3)

        if not find_and_click("Worlds", pid, "nav_menu.png"):
            print("Could not find 'Worlds' button. Retrying ESC...")
            vrcpilot.keyboard.press(vrcpilot.Key.ESCAPE, pid=pid)
            time.sleep(2)
            if not find_and_click("Worlds", pid, "nav_menu_retry.png"):
                continue
        time.sleep(3)

        find_and_click("Trending", pid, "worlds_list.png")
        time.sleep(3)

        card_x = 150 + (world_idx * 250)
        card_y = 400
        print(f"Clicking world card {world_idx} at ({card_x}, {card_y})...")
        vrcpilot.mouse.move(card_x, card_y, pid=pid)
        vrcpilot.mouse.click(vrcpilot.MouseButton.LEFT, pid=pid)
        time.sleep(3)

        if not find_and_click("Go", pid, "world_detail.png"):
            if not find_and_click("Join", pid, "world_detail_retry.png"):
                print("Could not find 'Go' or 'Join' button. Maybe already clicking?")

        print("Loading world (45s)...")
        time.sleep(45)

        take_photos(pid, world_idx)

    print("\nAll tasks completed successfully.")


if __name__ == "__main__":
    main()
