import solara
import leafmap.solara  # 確保引入這個模組

def create_split_map():
    # 1. 先建立一個標準的地圖物件，並強制設定中心點與縮放
    # 這裡的 center 是 [緯度, 經度]
    m = leafmap.Map(
        center=[23.665, 121.380], 
        zoom=14, 
        height="100%"
    )
    
    # 2. 在這個地圖物件上「套用」捲簾功能
    m.split_map(
        left_layer="Esri.WorldImagery",  # 左邊：衛星
        right_layer="OpenStreetMap",     # 右邊：街道
        left_label="衛星影像",
        right_label="街道地圖"
    )
    
    return m

@solara.component
def Page():
    # 3. 使用 use_memo 避免畫面重整時地圖重跑
    m = solara.use_memo(create_split_map, dependencies=[])

    with solara.Column(style={"height": "100vh", "padding": "0px"}):
        
        # 標題區塊
        with solara.Card(margin=2):
            solara.Markdown("## 🗺️ 馬太鞍溪 - 衛星/地圖對照")
            solara.Markdown("請拖曳地圖中央的分隔線，觀察地形與聚落差異。")

        # 4. 關鍵！使用 leafmap.solara.Map 來顯示
        # 這樣 Solara 才能正確解析地圖的設定
        leafmap.solara.Map(m)