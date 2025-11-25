import solara
import ipyleaflet  # 我們直接用底層套件，不透過 leafmap 轉一手

def create_split_map():
    # 1. 直接建立 ipyleaflet 地圖
    # 這是最底層的物件，Solara 對它的支援度最好
    m = ipyleaflet.Map(
        center=[23.665, 121.380],  # 馬太鞍溪座標
        zoom=13, 
        scroll_wheel_zoom=True,
        height="600px"
    )
    
    # 2. 定義左右兩張圖層
    # 左邊：衛星影像 (Esri World Imagery)
    left_layer = ipyleaflet.TileLayer(
        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        name="衛星影像"
    )
    
    # 右邊：街道地圖 (OpenStreetMap)
    right_layer = ipyleaflet.TileLayer(
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        name="街道地圖"
    )

    # 3. 建立捲簾控制器 (SplitMapControl)
    split_control = ipyleaflet.SplitMapControl(
        left_layer=left_layer, 
        right_layer=right_layer
    )
    
    # 4. 把控制器加到地圖上
    m.add_control(split_control)
    
    return m

@solara.component
def Page():
    # 使用 use_memo 鎖定地圖狀態
    m = solara.use_memo(create_split_map, dependencies=[])

    with solara.Column(style={"padding": "20px", "max-width": "1200px", "margin": "0 auto"}):
        
        solara.Markdown("## 🗺️ 馬太鞍溪 - 衛星/街道對照")
        solara.Markdown("請拖曳地圖中央的 **直線滑桿** 進行比對。")
        
        # 直接顯示 ipyleaflet 物件，這是最穩定的方式
        solara.display(m)