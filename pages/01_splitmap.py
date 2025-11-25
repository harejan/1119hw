import solara
import leafmap  # 👈 關鍵修正：只引入 leafmap，不要加 .solara

def create_split_map():
    # 建立地圖物件
    m = leafmap.Map(
        center=[23.665, 121.380], 
        zoom=14, 
        height="100%"
    )
    # 套用捲簾效果
    m.split_map(
        left_layer="Esri.WorldImagery",
        right_layer="OpenStreetMap",
        left_label="衛星影像",
        right_label="街道地圖"
    )
    return m

@solara.component
def Page():
    # 使用 use_memo 鎖住地圖，避免重整時消失
    m = solara.use_memo(create_split_map, dependencies=[])

    with solara.Column(style={"height": "100vh", "padding": "0px"}):
        with solara.Card(margin=2):
            solara.Markdown("## 🗺️ 馬太鞍溪 - 衛星/地圖對照")
            solara.Markdown("請拖曳地圖中央的分隔線，觀察地形與聚落差異。")

        # 👇 關鍵修正：使用 .element() 來顯示地圖
        # 這比 leafmap.solara.Map(m) 更穩定，絕對不會報錯
        m.element()