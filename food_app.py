import random
import json    # 👈 新增：用來處理 JSON 格式
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel  # 👈 新增這一行

class Restaurant(BaseModel):
    name: str
    transport: str
    type: str
    price: str
    rating: str
    ig_url: str

app = FastAPI(title="今天吃啥？")

# 🍔 虛擬餐廳資料庫 (維持原本的測試資料)
# 📂 設定我們要存檔的檔名
DB_FILE = "restaurants.json"

# 🛠️ 啟動時自動讀取資料庫的函數
def load_db():
    if os.path.exists(DB_FILE):
        # 如果檔案存在，就打開來讀取
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # 如果檔案不存在（第一次執行），給一些預設資料並立刻存檔
        default_data = [
            {"name": "巷口爆汁炸雞", "transport": "walk", "type": "fried", "price": "budget", "rating": "4.8", "ig_url": "#"},
            {"name": "慢活輕食沙拉吧", "transport": "walk", "type": "healthy", "price": "normal", "rating": "4.3", "ig_url": "#"}
        ]
        save_db(default_data)
        return default_data

# 🛠️ 儲存資料到檔案的函數
def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 讀取資料庫進來
RESTAURANT_DB = load_db()
@app.get("/", response_class=HTMLResponse)
def get_home():
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>今天吃啥？ - 專屬口袋名單抽籤</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        <style>
            .active-btn {
                background-color: black !important;
                color: white !important;
                border-color: black !important;
            }
        </style>
    </head>
    <body class="bg-gray-50 min-h-screen flex flex-col font-sans select-none antialiased">

        <header class="bg-white border-b-2 border-black sticky top-0 z-40 py-3 px-4 flex justify-between items-center shadow-sm">
            <h1 class="text-xl font-black tracking-wider text-gray-800">🤔 今天吃啥？</h1>
            <div class="flex gap-2">
                <button onclick="openListModal()" class="bg-gray-100 text-black px-3 py-2 rounded-xl font-bold text-sm shadow-sm hover:bg-gray-200 active:scale-95 transition-all border-2 border-black">
                    📜 名單
                </button>
                <button onclick="openModal()" class="bg-black text-white px-3 py-2 rounded-xl font-bold text-sm shadow-md hover:bg-gray-800 active:scale-95 transition-all border-2 border-black">
                    ➕ 新增
                </button>
            </div>
        </header>

        <main class="flex-grow flex items-center justify-center p-4">
            <div class="w-full max-w-md bg-white p-6 rounded-3xl border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
                
                <div class="mb-6">
                    <label class="block text-sm font-black text-gray-700 mb-2">📍 第一步：選擇交通方式</label>
                    <div class="grid grid-cols-3 gap-2">
                        <button onclick="selectOption('transport', 'walk', this)" class="transport-btn border-2 border-gray-300 py-3 rounded-2xl font-bold text-sm bg-white hover:bg-gray-50 active:scale-95 transition-all">🚶 走路</button>
                        <button onclick="selectOption('transport', 'bike', this)" class="transport-btn border-2 border-gray-300 py-3 rounded-2xl font-bold text-sm bg-white hover:bg-gray-50 active:scale-95 transition-all">🏍️ 騎車</button>
                        <button onclick="selectOption('transport', 'car', this)" class="transport-btn border-2 border-gray-300 py-3 rounded-2xl font-bold text-sm bg-white hover:bg-gray-50 active:scale-95 transition-all">🚗 開車</button>
                    </div>
                </div>

                <div class="mb-6">
                    <label class="block text-sm font-black text-gray-700 mb-2">🍟 第二步：今天想吃哪類？</label>
                    <div class="grid grid-cols-2 gap-2">
                        <button onclick="selectOption('type', 'fried', this)" class="type-btn border-2 border-gray-300 py-3 rounded-2xl font-bold text-sm bg-white hover:bg-gray-50 active:scale-95 transition-all">🍟 罪惡炸物</button>
                        <button onclick="selectOption('type', 'healthy', this)" class="type-btn border-2 border-gray-300 py-3 rounded-2xl font-bold text-sm bg-white hover:bg-gray-50 active:scale-95 transition-all">🥗 清淡健康</button>
                        <button onclick="selectOption('type', 'vegie', this)" class="type-btn border-2 border-gray-300 py-3 rounded-2xl font-bold text-sm bg-white hover:bg-gray-50 active:scale-95 transition-all">🥦 素食主義</button>
                        <button onclick="selectOption('type', 'noodle', this)" class="type-btn border-2 border-gray-300 py-3 rounded-2xl font-bold text-sm bg-white hover:bg-gray-50 active:scale-95 transition-all">🍜 麵食愛好</button>
                    </div>
                </div>

                <div class="mb-6">
                    <label class="block text-sm font-black text-gray-700 mb-2">💰 第三步：預算考量</label>
                    <div class="grid grid-cols-3 gap-2">
                        <button onclick="selectOption('price', 'budget', this)" class="price-btn border-2 border-gray-300 py-3 rounded-2xl font-bold text-xs bg-white hover:bg-gray-50 active:scale-95 transition-all">🪙 100元內</button>
                        <button onclick="selectOption('price', 'normal', this)" class="price-btn border-2 border-gray-300 py-3 rounded-2xl font-bold text-xs bg-white hover:bg-gray-50 active:scale-95 transition-all">🍱 200元內</button>
                        <button onclick="selectOption('price', 'luxury', this)" class="price-btn border-2 border-gray-300 py-3 rounded-2xl font-bold text-xs bg-white hover:bg-gray-50 active:scale-95 transition-all">💸 大餐500+</button>
                    </div>
                </div>

                <button onclick="startLottery()" class="w-full bg-blue-600 text-white py-4 rounded-2xl font-black text-lg shadow-md hover:bg-blue-700 active:scale-[0.98] transition-all mt-4 border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                    🎰 決定就是你了！
                </button>

                <div id="result-card" class="hidden mt-6 p-5 border-4 border-dashed border-green-500 rounded-2xl bg-green-50/50 text-center relative overflow-hidden">
                    <span class="absolute top-2 right-2 text-xs font-black bg-green-500 text-white px-2 py-0.5 rounded-full">開獎結果</span>
                    <h3 id="res-name" class="text-2xl font-black text-gray-800 mb-1">餐廳名稱</h3>
                    <div id="res-rating" class="text-yellow-500 font-bold text-sm mb-4">⭐ 5.0</div>
                    <a id="res-ig" href="#" target="_blank" class="inline-flex items-center gap-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold px-4 py-2.5 rounded-xl text-sm shadow-sm hover:opacity-90 active:scale-95 transition-all">
                        📸 查看儲存的 IG 貼文
                    </a>
                </div>

                <div id="error-card" class="hidden mt-6 p-4 border-2 border-red-500 rounded-2xl bg-red-50 text-center font-bold text-red-600 text-sm">
                    😢 糟糕！目前口袋名單中沒有同時符合這三個條件的餐廳，快去多存幾家貼文吧！
                </div>
            </div>
        </main>

        <div id="add-modal" class="fixed inset-0 bg-black/60 z-50 hidden flex items-center justify-center p-4 opacity-0 transition-opacity duration-300">
            <div class="bg-white w-full max-w-sm rounded-3xl p-6 border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] transform scale-95 transition-transform duration-300" id="modal-content">
                <h2 class="text-2xl font-black mb-4 border-b-2 border-gray-200 pb-2 flex items-center gap-2">✍️ 新增私房餐廳</h2>
                
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-1">餐廳名稱</label>
                        <input type="text" id="new-name" placeholder="例如：巷口無名滷肉飯" class="w-full border-2 border-gray-300 rounded-xl p-2.5 focus:border-black focus:outline-none font-bold">
                    </div>
                    
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-bold text-gray-700 mb-1">交通方式</label>
                            <select id="new-transport" class="w-full border-2 border-gray-300 rounded-xl p-2.5 focus:border-black focus:outline-none font-bold bg-white text-sm">
                                <option value="walk">🚶 走路</option>
                                <option value="bike">🏍️ 騎車</option>
                                <option value="car">🚗 開車</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-gray-700 mb-1">預算價格</label>
                            <select id="new-price" class="w-full border-2 border-gray-300 rounded-xl p-2.5 focus:border-black focus:outline-none font-bold bg-white text-sm">
                                <option value="budget">🪙 100元內</option>
                                <option value="normal">🍱 200元內</option>
                                <option value="luxury">💸 大餐500+</option>
                            </select>
                        </div>
                    </div>

                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-1">食物類型</label>
                        <select id="new-type" class="w-full border-2 border-gray-300 rounded-xl p-2.5 focus:border-black focus:outline-none font-bold bg-white text-sm">
                            <option value="fried">🍟 罪惡炸物</option>
                            <option value="healthy">🥗 清淡健康</option>
                            <option value="vegie">🥦 素食主義</option>
                            <option value="noodle">🍜 麵食愛好</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-1">IG 貼文連結 (選填)</label>
                        <input type="url" id="new-ig" placeholder="貼上 Instagram 網址..." class="w-full border-2 border-gray-300 rounded-xl p-2.5 focus:border-black focus:outline-none font-bold text-sm">
                    </div>
                </div>

                <div class="mt-6 flex gap-3">
                    <button onclick="closeModal()" class="flex-1 bg-gray-200 text-gray-800 py-3 rounded-xl font-bold hover:bg-gray-300 active:scale-95 transition-all border-2 border-transparent">
                        取消
                    </button>
                    <button onclick="submitNewRestaurant()" class="flex-1 bg-green-500 text-white py-3 rounded-xl font-bold border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:bg-green-600 active:scale-95 transition-all">
                        💾 儲存
                    </button>
                </div>
            </div>
        </div>
        <div id="list-modal" class="fixed inset-0 bg-black/60 z-50 hidden flex items-center justify-center p-4 opacity-0 transition-opacity duration-300">
            <div class="bg-white w-full max-w-sm rounded-3xl p-6 border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] max-h-[80vh] flex flex-col transform scale-95 transition-transform duration-300" id="list-modal-content">
                <h2 class="text-2xl font-black mb-4 border-b-2 border-gray-200 pb-2 flex justify-between items-center">
                    <span>📜 我的口袋名單</span>
                    <button onclick="closeListModal()" class="text-gray-400 hover:text-black font-bold text-sm">關閉</button>
                </h2>
                
                <div id="list-container" class="flex-grow overflow-y-auto space-y-3 pr-1">
                    </div>
            </div>
        </div>
        <script>
            // ─── 抽籤邏輯區 ───
            let selections = { transport: '', type: '', price: '' };

            function selectOption(category, value, element) {
                document.querySelectorAll('.' + category + '-btn').forEach(btn => {
                    btn.classList.remove('active-btn');
                });
                element.classList.add('active-btn');
                selections[category] = value;
            }

            async function startLottery() {
                if (!selections.transport || !selections.type || !selections.price) {
                    alert('請先填滿三個關卡，再開始進行開獎唷！');
                    return;
                }
                document.getElementById('result-card').classList.add('hidden');
                document.getElementById('error-card').classList.add('hidden');

                const response = await fetch(`/draw?transport=${selections.transport}&type=${selections.type}&price=${selections.price}`);
                const data = await response.json();

                if (data.status === 'success') {
                    document.getElementById('res-name').innerText = data.data.name;
                    document.getElementById('res-rating').innerText = '⭐ ' + data.data.rating;
                    document.getElementById('res-ig').href = data.data.ig_url;
                    document.getElementById('result-card').classList.remove('hidden');
                } else {
                    document.getElementById('error-card').classList.remove('hidden');
                }
            }

            // ─── 表單 Modal 控制邏輯區 ───
            
            // 開啟表單 (加入滑順動畫)
            function openModal() {
                const modal = document.getElementById('add-modal');
                modal.classList.remove('hidden');
                // 微小延遲讓 CSS 動畫生效
                setTimeout(() => {
                    modal.classList.remove('opacity-0');
                    document.getElementById('modal-content').classList.remove('scale-95');
                }, 10);
            }

            // 關閉表單
            function closeModal() {
                const modal = document.getElementById('add-modal');
                modal.classList.add('opacity-0');
                document.getElementById('modal-content').classList.add('scale-95');
                // 等待淡出動畫結束後再隱藏
                setTimeout(() => {
                    modal.classList.add('hidden');
                }, 300);
            }

            // 模擬點擊儲存按鈕
            async function submitNewRestaurant() {
                // 抓取所有輸入框的值
                const name = document.getElementById('new-name').value;
                const transport = document.getElementById('new-transport').value;
                const price = document.getElementById('new-price').value;
                const type = document.getElementById('new-type').value;
                const ig_url = document.getElementById('new-ig').value || "#";

                if(!name) {
                    alert("請至少輸入餐廳名稱喔！");
                    return;
                }

                // 打包成 JSON 格式
                const newData = { 
                    name: name, 
                    transport: transport, 
                    type: type, 
                    price: price, 
                    rating: "5.0", // 新增的預設給 5 星好評！
                    ig_url: ig_url 
                };

                // 透過 POST 請求發送給 Python 後端
                const response = await fetch('/add', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(newData)
                });

                if(response.ok) {
                    alert("🎉 成功加入口袋名單！");
                    closeModal();
                    // 清空輸入框，方便下次輸入
                    document.getElementById('new-name').value = '';
                    document.getElementById('new-ig').value = '';
                }
            }
            // ─── 查看名單 Modal 控制邏輯區 ───

            // 1. 開啟名單並從後端抓資料
            async function openListModal() {
                const modal = document.getElementById('list-modal');
                const container = document.getElementById('list-container');
                container.innerHTML = "⌛ 載入中..."; // 載入中的小提示

                // 顯示視窗與動畫
                modal.classList.remove('hidden');
                setTimeout(() => {
                    modal.classList.remove('opacity-0');
                    document.getElementById('list-modal-content').classList.remove('scale-95');
                }, 10);

                // 向 Python API 要所有餐廳資料
                const response = await fetch('/all');
                const result = await response.json();

                if (result.status === 'success') {
                    container.innerHTML = ""; // 清空文字

                    // 如果沒餐廳，顯示客氣的提示
                    if (result.data.length === 0) {
                        container.innerHTML = "<p class='text-gray-400 text-center py-4 font-bold text-sm'>目前名單空空如也...</p>";
                        return;
                    }

                    // 🛠️ 用迴圈把每家餐廳拼成漂亮的 HTML 卡片
                    result.data.forEach(res => {
                        // 轉換標籤文字讓畫面更好看
                        const transMap = { walk: "🚶 走路", bike: "🏍️ 騎車", car: "🚗 開車" };
                        const priceMap = { budget: "🪙 銅板", normal: "🍱 平價", luxury: "💸 大餐" };

                        const card = `
                            <div class="border-2 border-black p-3 rounded-xl bg-gray-50 flex justify-between items-center">
                                <div>
                                    <h4 class="font-black text-gray-800">${res.name}</h4>
                                    <p class="text-xs text-gray-500 font-bold mt-1">
                                        ${transMap[res.transport] || res.transport} | ${priceMap[res.price] || res.price}
                                    </p>
                                </div>
                                <div class="flex gap-1 items-center">
                                    ${res.ig_url !== '#' ? `
                                        <a href="${res.ig_url}" target="_blank" class="text-xs bg-pink-100 text-pink-600 font-black px-2 py-1 rounded-md border border-pink-300 hover:bg-pink-200">IG</a>
                                    ` : ''}
                                    <button onclick="deleteRestaurant('${res.name}')" class="text-xs bg-red-50 text-red-500 font-black px-2 py-1 rounded-md border border-red-200 hover:bg-red-100 active:scale-95 transition-all">🗑️</button>
                                </div>
                            </div>
                        `;
                        container.innerHTML += card; // 塞進大盒子裡
                    });
                }
            }

            // 2. 關閉名單視窗
            function closeListModal() {
                const modal = document.getElementById('list-modal');
                modal.classList.add('opacity-0');
                document.getElementById('list-modal-content').classList.add('scale-95');
                setTimeout(() => { modal.classList.add('hidden'); }, 300);
            }
            // 👈 新增：點擊垃圾桶時發送刪除請求給 Python
            async function deleteRestaurant(name) {
                // 彈出瀏覽器內建的確認視窗，防止手誤點錯
                if (!confirm(`確定要將【${name}】從口袋名單中移除嗎？`)) {
                    return;
                }

                // 發送 POST 請求給後端，並把餐廳名稱當作參數傳過去
                const response = await fetch(`/delete?name=${encodeURIComponent(name)}`, {
                    method: 'POST'
                });
                const result = await response.json();

                if (result.status === 'success') {
                    // 刪除成功後，重新呼叫一次 openListModal() 刷新畫面名單！
                    openListModal();
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

@app.get("/draw")
def draw_restaurant(transport: str, type: str, price: str):
    filtered_list = [
        res for res in RESTAURANT_DB 
        if res["transport"] == transport and res["type"] == type and res["price"] == price
    ]
    if filtered_list:
        chosen = random.choice(filtered_list)
        return {"status": "success", "data": chosen}
    else:
        return {"status": "error", "message": "No restaurant matches filters."}
# 👈 新增這個接收資料的通道
@app.post("/add")
def add_restaurant(new_res: Restaurant):
    # 1. 塞進記憶體的名單裡
    RESTAURANT_DB.append(new_res.model_dump())
    
    # 2. 👈 新增這行：同步寫入硬碟的 JSON 檔案中永久保存！
    save_db(RESTAURANT_DB)
    
    return {"status": "success", "message": "成功加入名單並已存檔！"}
# 👈 新增這個通道，用來獲取所有餐廳名單
@app.get("/all")
def get_all_restaurants():
    # 直接把我們記憶體裡的所有餐廳資料回傳給前端
    return {"status": "success", "data": RESTAURANT_DB}
# 👈 新增這個通道，用來刪除指定餐廳
@app.post("/delete")
def delete_restaurant(name: str):
    global RESTAURANT_DB
    # 篩選掉名字和前端傳過來一樣的那家餐廳
    RESTAURANT_DB = [res for res in RESTAURANT_DB if res["name"] != name]
    # 同步更新硬碟裡的 JSON 檔案
    save_db(RESTAURANT_DB)
    return {"status": "success", "message": f"已成功刪除 {name}"}