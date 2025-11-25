import solara
import leafmap

# 建立地圖的函式
def create_split_map():
    # 建立一個捲簾地圖物件
    # 注意：這裡將中心點微調至 23.665, 121.380 (光復馬太鞍溪橋/濕地附近)
    m = leafmap.Map(center=[23.665, 121.380], zoom=14, height="650px")
    
    m.split_map(
        left_layer="Esri.WorldImagery",  # 左側：衛星影像
        right_layer="OpenStreetMap",     # 右側：街道地圖
        left_label="衛星影像",
        right_label="街道地圖"
    )
    
    return m

@solara.component
def Page():
    m = solara.use_memo(create_split_map, dependencies=[])

    with solara.Column(style={"width": "100%", "height": "100vh"}):
        solara.Markdown("## 🗺️ 馬太鞍溪 - 衛星與地圖對照")
        solara.Markdown("拖曳中間的分隔線，比較當地的**地形地貌 (衛星)** 與 **聚落道路 (街道)** 分布。")
        
        # 顯示地圖元件
        # 在 Solara 中顯示 ipyleaflet 地圖需使用 .element() 或 solara.display()
        # leafmap 的 Map 物件相容於 ipyleaflet
        m.element()