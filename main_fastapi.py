import numpy as np
import cv2
import base64
from fastapi import FastAPI, File, UploadFile
from fastapi import Request

# 开发前端界面
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# 定义fastapi的启动app
app = FastAPI()

# 解除跨域访问限制
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义访问接口
@app.post("/animegan/")
async def processimg(request: Request, file: UploadFile = File(...)):
    #  接收前端上传的图片
    imgdata = await file.read()
    imgdata = np.frombuffer(imgdata, np.uint8)
    img = cv2.imdecode(imgdata, cv2.IMREAD_COLOR)
    if img is None:
        print("文件格式错误")
        return {"state": -1}
    # 照片算法处理
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    comp = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # 返回处理后的图像数据
    _, buffer_img = cv2.imencode('.jpg', comp)
    img64 = base64.b64encode(buffer_img)
    img64 = str(img64, encoding='utf-8')
    return {"state": 1, "img": img64}


# 挂载静态资源目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 定义页面模板库位置
templates = Jinja2Templates(directory="templates")

# 定义首页
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, })
