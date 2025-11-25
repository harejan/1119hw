import solara
import leafmap.maplibregl as leafmap
import os

# 1. 讀取 API Key
MAPTILER_KEY = os.environ.get("MAPTILER_API_KEY", "")

def create_3d_map():
    # 2. 檢查 Key 是否存在
    if not MAPTILER_KEY:
        m = leafmap.Map(
            center=[121.380, 23.665],
            zoom=12,
            style="https://demotiles.maplibre.org/style.json",
        )
        return m

    # 3. 設定 MapTiler 衛星影像樣式
    style_url = f"https://api.maptiler.com/maps/hybrid/style.json?key={MAPTILER_KEY}"

    m = leafmap.Map(
        style=style_url,
        center=[121.350, 23.680],
        zoom=12.5,
        pitch=75,    # 傾斜角度
        bearing=130, # 旋轉角度
    )
    
    # --- 關鍵修正：改用原生的 add_source 與 set_terrain ---
    
    # 步驟 A: 加入地形資料源 (Source)
    # 我們使用 MapTiler 提供的 Terrain-RGB 資料
    m.add_source("maptiler-terrain", {
        "type": "raster-dem",
        "url": f"https://api.maptiler.com/tiles/terrain-rgb/tiles.json?key={MAPTILER_KEY}",
        "tileSize": 512,
        "maxzoom": 14
    })
    
    # 步驟 B: 啟用該地形 (Set Terrain)
    # exaggeration 是誇大係數，1.5 倍讓山看起來更立體
    m.set_terrain({"source": "maptiler-terrain", "exaggeration": 1.5})
    
    # 加入導航控制項
    m.add_control("navigation", position="top-right")
    
    return m

@solara.component
def Page():
    with solara.Column(style={"height": "100vh", "padding": "0px"}):
        
        with solara.Card(margin=2):
            solara.Markdown("## 🏔️ 馬太鞍溪 3D 地形模擬")
            if not MAPTILER_KEY:
                solara.Error("⚠️ 請設定 MapTiler API Key 以檢視 3D 地形。")
            else:
                solara.Markdown("按住 **滑鼠右鍵** 拖曳可旋轉視角。")

        # 顯示地圖
        m = create_3d_map()
        solara.display(m)