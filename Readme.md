# FastAPI Project

Simple backend API sử dụng **FastAPI** và **Uvicorn**.

---

## 1. Yêu cầu hệ thống

* Python ≥ 3.10
* pip

Kiểm tra:

```bash
python --version
pip --version
```

---

## 2. Cài đặt dependencies

Tạo virtual environment (khuyến nghị):

```bash
python -m venv venv
```

Kích hoạt môi trường:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

Cài thư viện:

```bash
pip install -r requirements.txt
```

---

## 3. Chạy project

Start server:

```bash
uvicorn src:app --reload
```

Giải thích:

* `main` → file `main.py`
* `app` → biến FastAPI instance
* `--reload` → tự restart khi code thay đổi

---

## 4. Truy cập API

Sau khi chạy server:

```
http://127.0.0.1:8000
```

API docs tự động:

* Swagger UI

```
http://127.0.0.1:8000/docs
```

* ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## 6. Export dependencies

Nếu thêm thư viện mới:

```bash
pip freeze > requirements.txt
```

---

