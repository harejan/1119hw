FROM python:3.11

# 設定工作目錄
WORKDIR /code

# --- ⚡️ 焦土政策安裝法 ⚡️ ---
# 我們不讀取 requirements.txt 了，直接在這裡寫死版本
# 這樣絕對不會有舊版本來搗亂
RUN pip install --no-cache-dir "leafmap>=0.50.0" solara pandas

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