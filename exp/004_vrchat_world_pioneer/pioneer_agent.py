import time
import os
from datetime import datetime
from pathlib import Path
import vrcpilot

class WorldPioneer:
    def __init__(self, base_dir="exp/004_vrchat_world_pioneer"):
        self.base_dir = Path(base_dir)
        self.output_dir = self.base_dir / "output" / datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.photo_count = 0
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def capture_evidence(self, pid, label="photo"):
        self.photo_count += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.photo_count:03d}_{label}_{timestamp}.png"
        filepath = self.output_dir / filename
        
        img = vrcpilot.take_screenshot(pid=pid)
        img.save(filepath)
        self.log(f"Saved evidence: {filepath}")
        return filepath

    def find_and_click(self, pid, text_query, timeout=15):
        self.log(f"Searching for UI element: '{text_query}'")
        start_time = time.time()
        while time.time() - start_time < timeout:
            img = vrcpilot.take_screenshot(pid=pid)
            result = vrcpilot.ocr(img)
            for word in result.words:
                if text_query.lower() in word.text.lower():
                    x, y, w, h = word.bbox
                    cx, cy = int(x + w / 2), int(y + h / 2)
                    vrcpilot.mouse.move(cx, cy, pid=pid)
                    vrcpilot.mouse.click(pid=pid)
                    self.log(f"Clicked '{word.text}' at ({cx}, {cy})")
                    return True
            time.sleep(1)
        return False

    def run_crate_game_experiment(self, pid):
        self.log("--- Starting 'A Game About Crates' Automation Experiment ---")
        vrcpilot.focus(pid=pid)
        
        # 1. 初期状態の記録
        self.capture_evidence(pid, "initial_state")
        
        # 2. OCRで「Crate」や「Open」を読み取ってクリックするループ (簡易版)
        for i in range(5):
            self.log(f"Interaction cycle {i+1}/5")
            if self.find_and_click(pid, "Open"):
                time.sleep(2)
                self.capture_evidence(pid, f"crate_opened_{i+1}")
            else:
                self.log("Target 'Open' not found, performing random click exploration.")
                vrcpilot.mouse.move(640, 360, pid=pid)
                vrcpilot.mouse.click(pid=pid)
            time.sleep(2)

        # 3. 最終結果の記録
        self.capture_evidence(pid, "final_wealth_status")
        self.log("Experiment completed.")

def main():
    pioneer = WorldPioneer()
    # AI専用のプロフィール (10) を使用して、ユーザーの本アカウントと分離
    pioneer.log("Launching VRChat with AI Profile (10)...")
    
    pid = vrcpilot.launch(
        no_vr=True,
        profile=10,
        screen_width=1280,
        screen_height=720,
    )
    
    pioneer.log("Waiting for VRChat to stabilize (45s)...")
    time.sleep(45)
    
    try:
        pioneer.run_crate_game_experiment(pid)
    except Exception as e:
        pioneer.log(f"Error during experiment: {e}")
    finally:
        pioneer.log(f"All artifacts saved in: {pioneer.output_dir}")

if __name__ == "__main__":
    main()
