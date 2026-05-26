import time
from pathlib import Path
import vrcpilot
from PIL import Image

def is_green(pixel):
    r, g, b = pixel
    # 緑色が優勢かつ一定以上の輝度があるか判定 (環境に合わせて調整が必要な可能性あり)
    return g > 150 and r < 100 and b < 100

def run_reflex_test(pid):
    print("--- Reflex Test: Target 0ms ---")
    vrcpilot.focus(pid=pid)
    time.sleep(1)

    # 1. スタートボタンをクリック (座標は一般的な1280x720のワールド中央付近を想定)
    # 実際にはOCRで "Start" を探すべきだが、最速を目指すため一旦固定
    print("Clicking Start...")
    vrcpilot.mouse.move(640, 360, pid=pid)
    vrcpilot.mouse.click(pid=pid)
    
    print("Waiting for the signal (Red -> Green)...")
    
    # 2. 高速ループで画面中央のピクセルを監視
    # take_screenshot よりも高速な get_pixel (実装されている場合) または最小範囲のキャプチャを使用
    start_time = time.time()
    try:
        while True:
            # 画面中央 (640, 360) の色を取得
            shot = vrcpilot.take_screenshot(pid=pid)
            if shot is None:
                print("Failed to capture screenshot. Window might be closed.")
                break
                
            h, w = shot.image.shape[:2]
            if h < 361 or w < 641:
                print(f"Waiting for valid window size... (Current: {w}x{h})")
                time.sleep(1)
                continue

            # Screenshot.image は (H, W, 3) の numpy array (RGB)
            pixel = shot.image[360, 640]
            
            if is_green(pixel):
                # 3. 緑になった瞬間にクリック
                vrcpilot.mouse.click(pid=pid)
                print(f"!!! TRIGGERED !!!")
                break
                
            # CPU負荷を抑えつつ最速を目指す
            time.sleep(0.001) 
            
    except KeyboardInterrupt:
        print("Test cancelled.")
        return

    # 4. 証拠写真を撮影
    print("Taking evidence photo in 2 seconds...")
    time.sleep(2)
    evidence_img = vrcpilot.take_screenshot(pid=pid)
    evidence_path = Path("reflex_result_0ms.png")
    evidence_img.save(evidence_path)
    print(f"Evidence saved to {evidence_path}")

def main():
    # AI専用のプロフィール (10) を使用して、ユーザーの本アカウントと分離
    print("Launching VRChat with AI Profile (10)...")
    pid = vrcpilot.launch(
        no_vr=True,
        profile=10,
        screen_width=1280,
        screen_height=720,
    )
    
    print("Waiting for VRChat to stabilize (30s)...")
    time.sleep(30)
    
    run_reflex_test(pid)

if __name__ == "__main__":
    main()
