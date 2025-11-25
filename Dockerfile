FROM python:3.11

# 設定工作目錄
WORKDIR /code

# --- 關鍵：讀取你的 requirements.txt ---
COPY ./requirements.txt /code/requirements.txt

# 安裝清單內的所有套件 (包含 ipyleaflet, geopandas 等)
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 建立使用者
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    SOLARA_ASSETS_PROXY=False

# 複製程式碼
COPY --chown=user . /code

# 啟動指令
CMD ["solara", "run", "./pages", "--host=0.0.0.0", "--port=7860"]