import solara
import leafmap

def create_split_map():
    # 1. 建立地圖
    m = leafmap.Map(
        center=[23.665, 121.380], 
        zoom=13, 
        height="600px",
        draw_control=False,
        measure_control=False
    )
    
    # 2. 加入捲簾特效
    try:
        m.split_map(
            left_layer="Esri.WorldImagery",
            right_layer="OpenStreetMap",
            left_label="衛星影像",
            right_label="街道地圖"
        )
    except Exception as e:
        print(f"Split map error: {e}")

    # --- 關鍵修正：強迫地圖「記住」位置 ---
    # 有時候加入特效後，地圖會重置，所以我們這裡再鎖定一次
    m.set_center(23.665, 121.380)
    m.set_zoom(13)
    
    return m

@solara.component
def Page():
    # 使用 use_memo 確保地圖只建立一次
    m = solara.use_memo(create_split_map, dependencies=[])

    with solara.Column(style={"padding": "20px", "max-width": "1200px", "margin": "0 auto"}):
        
        solara.Markdown("## 🗺️ 馬太鞍溪 - 衛星/街道對照")
        solara.Markdown("請拖曳地圖中央的 **直線滑桿** 進行比對。")
        
        # --- 關鍵修正：改用 solara.display ---
        # 這對 ipyleaflet 的複雜控制項支援度較好
        solara.display(m)