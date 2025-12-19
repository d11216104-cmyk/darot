# darot

撲克牌十點半 (10.5) 遊戲

## 遊戲規則

- A = 1 點
- J, Q, K = 0.5 點
- 數字牌 = 面值
- 目標：接近 10.5 但不超過

## 安裝

```bash
pip install -r requirements.txt
```

## 使用方式

### 純網頁版本（推薦，無需伺服器）

直接在瀏覽器中開啟 `game.html` 檔案即可遊玩，無需安裝任何套件或啟動伺服器。

### 命令列版本

```bash
python ten_point_five.py
```

### 網頁伺服器版本

```bash
pip install -r requirements.txt
python server.py
```

然後在瀏覽器中開啟 `http://localhost:5000`