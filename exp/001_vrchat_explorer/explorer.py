import time

import vrcpilot


def find_and_click(text_query, pid, screenshot_name="debug.png", timeout=10):
    print(f"Searching for '{text_query}'...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        img = vrcpilot.take_screenshot(pid=pid)
        img.save(screenshot_name)
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


def main():
    print("--- VRChat Explorer Agent ---")
    pid = vrcpilot.launch(
        no_vr=True,
        profile=10,
        screen_width=1280,
        screen_height=720,
        wait_timeout=60,
    )
    print(f"Step 1: VRChat launched. PID: {pid}")

    print("Step 2: Waiting for initialization (45s)...")
    time.sleep(45)

    vrcpilot.focus(pid=pid)

    print("Step 3: Opening Main Menu...")
    vrcpilot.keyboard.press("esc")
    time.sleep(3)

    if not find_and_click("Worlds", pid, "1_menu.png"):
        print("Failed to find 'Worlds' in menu. Retrying ESC...")
        vrcpilot.keyboard.press("esc")
        time.sleep(2)
        if not find_and_click("Worlds", pid, "1_retry_menu.png"):
            print("Could not find Worlds. Exiting.")
            return

    time.sleep(5)

    print("Step 4: Looking for world categories...")
    if not find_and_click("New", pid, "2_worlds.png"):
        print("'New' not found, trying 'Trending'...")
        find_and_click("Trending", pid, "2_worlds_alt.png")

    time.sleep(5)

    print("Step 5: Clicking a world card...")
    vrcpilot.mouse.move(640, 360, pid=pid)
    vrcpilot.mouse.click(vrcpilot.MouseButton.LEFT, pid=pid)
    time.sleep(3)

    print("Step 6: Joining World...")
    if not find_and_click("Go", pid, "3_world_detail.png"):
        find_and_click("Join", pid, "3_world_detail_alt.png")

    print("Step 7: Waiting for world to load (30s)...")
    time.sleep(30)

    print("Step 8: Taking memorial photo...")
    final_img = vrcpilot.take_screenshot(pid=pid)
    final_img.save("memorial_photo.png")
    print("Success! Memorial photo saved as 'memorial_photo.png'.")


if __name__ == "__main__":
    main()
