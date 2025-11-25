FROM python:3.11

# 設定工作目錄
WORKDIR /code

# --- ⚡️ 強制刷新區塊 ⚡️ ---
# 只要改變下面這行日期，Docker 就會被迫重新下載所有套件
# 這能解決 "ModuleNotFoundError" 的問題
ENV REFRESHED_AT=2025-11-25_V2

# 強制安裝最新版 leafmap (大於 0.50.0 絕對支援 solara)
RUN pip install --no-cache-dir "leafmap>=0.50.0" solara pandas

# 複製 requirements.txt (作為備用)
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 建立使用者 (Hugging Face 安全規範)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    SOLARA_ASSETS_PROXY=False

# 複製程式碼
COPY --chown=user . /code

# 啟動指令
# 注意：你的檔案現在可能叫 01_splitmap.py，指向 pages 資料夾最保險
CMD ["solara", "run", "./pages", "--host=0.0.0.0", "--port=7860"]