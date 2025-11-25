import solara
import leafmap.maplibregl as leafmap
import os

# 1. 讀取你在 Hugging Face 設定的密鑰
MAPTILER_KEY = os.environ.get("MAPTILER_API_KEY", "")

def create_3d_map():
    # 2. 檢查是否有 Key，沒有的話顯示警告地圖
    if not MAPTILER_KEY:
        # 回傳一個預設的平面地圖
        m = leafmap.Map(
            center=[121.380, 23.665], # [經度, 緯度]
            zoom=12,
            style="https://demotiles.maplibre.org/style.json",
        )
        m.add_control("fullscreen")
        return m

    # 3. 設定 MapTiler 的 3D 地形樣式
    style_url = f"https://api.maptiler.com/maps/satellite/style.json?key={MAPTILER_KEY}"

    # 4. 建立 3D 地圖
    m = leafmap.Map(
        style=style_url,
        # --- 關鍵座標修正 ---
        # 馬太鞍溪上游視角
        center=[121.350, 23.680], # [經度, 緯度] 注意順序！
        zoom=12.5,
        pitch=75,    # 傾斜 75 度 (像鳥一樣俯衝的視角)
        bearing=130, # 旋轉角度 (面向東南方，看往下游光復市區)
    )
    
    # 5. 啟用地形效果 (Exaggeration=1.5 讓山脈看起來更立體一點)
    m.add_terrain(
        source="maptiler_terrain", 
        exaggeration=1.5
    )
    
    # 加入導航控制項
    m.add_control("navigation", position="top-right")
    
    return m

@solara.component
def Page():
    with solara.Column(style={"height": "100vh", "padding": "0px"}):
        
        # 標題區
        with solara.Card(margin=2):
            solara.Markdown("## 🏔️ 馬太鞍溪 3D 地形模擬")
            if not MAPTILER_KEY:
                solara.Error("⚠️ 尚未設定 MapTiler API Key，目前僅顯示 2D 平面圖。請至 Hugging Face Settings 加入 Secret。")
            else:
                solara.Markdown("按住 **右鍵拖曳** 可旋轉視角 (Pitch/Bearing)，觀察上游崩塌地形與下游沖積扇的高低差。")

        # 顯示地圖
        # 使用 solara.display() 比較穩定
        m = create_3d_map()
        solara.display(m)