import solara
import leafmap.solara

# --- 1. 設定地理資訊 (花蓮馬太鞍溪上游示意點) ---
# 堰塞湖模擬位置
LAKE_LAT = 23.685
LAKE_LON = 121.380

# 地圖中心 (稍微往東南移，讓使用者能看到下游光復市區)
MAP_CENTER = [23.675, 121.40]
DEFAULT_ZOOM = 13

@solara.component
def Page():
    # --- 2. 狀態管理 (Reactivity) ---
    # 控制水位高度 (預設 50 公尺)
    water_level, set_water_level = solara.use_state(50)
    # 控制是否顯示衛星圖
    show_satellite, set_show_satellite = solara.use_state(True)

    # --- 3. 頁面排版 ---
    with solara.Column(style={"height": "100vh", "padding": "0px"}):
        
        # 標題與控制面板 (浮動卡片風格)
        with solara.Card(elevation=2, margin=2):
            solara.Markdown("# 🌊 花蓮馬太鞍溪 - 堰塞湖監測系統")
            
            with solara.Row():
                # A. 顯示數值
                solara.Info(f"目前模擬水位： {water_level} 公尺", icon=True)
                
                # B. 判斷危險等級
                if water_level > 80:
                    solara.Error("🔴 危險等級：極高 (立即撤離)")
                elif water_level > 60:
                    solara.Warning("🟠 危險等級：警戒 (準備撤離)")
                else:
                    solara.Success("🟢 危險等級：觀察中")

            # C. 互動滑桿
            solara.SliderInt(
                label="模擬水位高度 (調整以此預測影響範圍)", 
                value=water_level, 
                min=10, 
                max=100, 
                on_value=set_water_level
            )
            
            # D. 地圖切換開關
            solara.Checkbox(label="開啟衛星影像 (Satellite)", value=show_satellite, on_value=set_show_satellite)

        # --- 4. 地圖繪製 ---
        # 每次 water_level 改變，這個函式就會重新執行，地圖圈圈會變大
        m = leafmap.Map(center=MAP_CENTER, zoom=DEFAULT_ZOOM)

        # 根據開關決定底圖
        if show_satellite:
            m.add_basemap("HYBRID")
        else:
            m.add_basemap("OpenStreetMap")

        # 標示堰塞湖位置 (崩塌點)
        m.add_marker(
            location=[LAKE_LAT, LAKE_LON],
            tooltip="堰塞湖堵塞點",
            popup="<b>馬太鞍溪上游崩塌處</b><br>土石堆積造成河道堵塞",
            icon="exclamation-triangle",
            icon_color="red"
        )

        # 繪製動態警戒範圍 (半徑隨水位變大)
        # 公式只是模擬用：水位 * 30 (例如 50m 水位 = 1500m 半徑)
        danger_radius = water_level * 30
        
        m.add_circle(
            location=[LAKE_LAT, LAKE_LON],
            radius=danger_radius,
            color="red",
            fill_color="orange",
            fill_opacity=0.4,
            popup=f"預估淹沒/影響範圍 (半徑 {danger_radius} 公尺)"
        )

        # 顯示地圖元件
        leafmap.solara.Map(m)

# 本地測試用
if __name__ == "__main__":
    solara.run(Page)