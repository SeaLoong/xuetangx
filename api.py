import random
import string

import httputils
import time


class API:
    client = None

    def __init__(self, headers=None, cookies=None):
        self.client = httputils.Client(headers, cookies)

    async def close(self):
        await self.client.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self):
        await self.client.close()

    async def header_ajax(self):
        r = await self.client.get("/header_ajax", headers={
            "x-referer": "https://scutspoc.xuetangx.com/#/home",
            "Referer": "https://scutspoc.xuetangx.com/",
            "X-CSRFToken": ""
        })
        return await r.json()

    async def captcha(self):
        r = await self.client.get("/api/v1/code/captcha", headers={
            "x-referer": "https://scutspoc.xuetangx.com/#/home",
            "Referer": "https://scutspoc.xuetangx.com/",
            "X-CSRFToken": ""
        })
        return await r.json()

    async def login(self, username: str, password: str, _captcha: str):
        r = await self.client.post("/api/v1/oauth/number/login", {
            "username": username,
            "password": password,
            "captcha": _captcha,
            "captcha_key": ""
        }, headers={
            "Origin": "https://scutspoc.xuetangx.com",
            "x-referer": "https://scutspoc.xuetangx.com/#/home",
            "Referer": "https://scutspoc.xuetangx.com/",
            "X-CSRFToken": ""
        })
        return r.status == 200

    async def plat_term(self, plat_id):
        r = await self.client.get("/api/v1/plat_term", {
            "plat_id": plat_id
        }, headers={
            "x-referer": "https://scutspoc.xuetangx.com/manager#/studentcourselist",
            "Referer": "https://scutspoc.xuetangx.com/manager",
            "X-CSRFToken": ""
        })
        return await r.json()

    async def mycourse_list(self, term_id):
        r = await self.client.get("/mycourse_list", {
            "running_status": "",
            "term_id": term_id,
            "search": "",
            "page_size": 10,
            "page": 1
        }, headers={
            "x-referer": "https://scutspoc.xuetangx.com/manager#/studentcourselist",
            "Referer": "https://scutspoc.xuetangx.com/manager",
            "X-CSRFToken": ""
        })
        return await r.json()

    async def score(self, course_id, class_id):
        r = await self.client.get("/score/" + course_id + "/", {
            "class_id": class_id,
            "if_cache": 1
        }, headers={
            "x-referer": "https://scutspoc.xuetangx.com/lms#/" + course_id + "/" + class_id + "/schedule/",
            "Referer": "https://scutspoc.xuetangx.com/lms"
        })
        return await r.json()

    async def courseware(self, course_id, class_id: str):
        r = await self.client.post("/lms/api/v1/course/" + course_id + "/courseware", {
            "class_id": class_id
        }, headers={
            "x-referer": "https://scutspoc.xuetangx.com/lms#/" + course_id + "/" + class_id + "/schedule/",
            "Referer": "https://scutspoc.xuetangx.com/lms",
            "Origin": "https://scutspoc.xuetangx.com"
        })
        return await r.json()

    async def study_record(self, course_id, class_id):
        r = await self.client.get("/lms/api/v1/study_record/" + course_id + "/", {
            "course_id": course_id,
            "class_id": class_id
        }, headers={
            "Accept": "*/*",
            "x-referer": "https://scutspoc.xuetangx.com/lms#/" + course_id + "/" + class_id + "/schedule/",
            "Referer": "https://scutspoc.xuetangx.com/lms"
        })
        return await r.json()

    async def get_video_watched_record(self, course_id, class_id, unit_id, video_id):
        r = await self.client.get("/video_point/get_video_watched_record", {
            "cid": course_id,
            "vtype": "rate",
            "video_type": "video"
        }, headers={
            "Accept": "*/*",
            "x-referer": "https://scutspoc.xuetangx.com/lms#/" + course_id + "/" + class_id + "/"
                         + unit_id + "/" + video_id + "/0/handouts",
            "Referer": "https://scutspoc.xuetangx.com/lms"
        })
        return await r.json()

    async def class_videos(self, course_id, class_id, unit_id, video_id):
        r = await self.client.get("/server/api/class_videos/", {
            "video_id": video_id,
            "class_id": class_id
        }, headers={
            "Accept": "*/*",
            "x-referer": "https://scutspoc.xuetangx.com/lms#/" + course_id + "/" + class_id + "/"
                         + unit_id + "/" + video_id + "/0/handouts",
            "Referer": "https://scutspoc.xuetangx.com/lms"
        })
        return await r.json()

    async def homework_status(self, course_id: str, class_id, homework_list: list):
        r = await self.client.post("/inner_api/homework/status/", {
            "homework_list": homework_list,
            "course_id": course_id
        }, headers={
            "x-referer": "https://scutspoc.xuetangx.com/lms#/" + course_id + "/" + class_id + "/schedule/",
            "Referer": "https://scutspoc.xuetangx.com/lms",
            "Origin": "https://scutspoc.xuetangx.com"
        })
        return await r.json()

    async def homework_result(self, course_id, class_id, homework_id: str, paper_id: str):
        r = await self.client.get("/inner_api/homework/score/result/" + paper_id + "/" + homework_id + "/", headers={
            "x-referer": "https://scutspoc.xuetangx.com/lms#/" + course_id + "/" + class_id + "/homeworkList" +
                         "/analysis/" + paper_id + "/" + homework_id,
            "Referer": "https://scutspoc.xuetangx.com/lms"
        })
        return await r.json()

    async def homework_subject(self, course_id: str, class_id: str, homework_id: str):
        r = await self.client.post("/inner_api/homework/paper/subject/", {
            "class_id": class_id,
            "homework_id": homework_id,
            "product_id": course_id
        }, headers={
            "x-referer": "https://scutspoc.xuetangx.com/lms#/" + course_id + "/" + class_id + "/homeworkList" +
                         "/homework/" + homework_id,
            "Referer": "https://scutspoc.xuetangx.com/lms",
            "Origin": "https://scutspoc.xuetangx.com"
        })
        return await r.json()

    async def homework_answer(self, course_id: str, class_id, homework_id, user_homework_id: int,
                              question_record_id: int, answers):
        r = await self.client.post("/inner_api/homework/question/answer/", {
            "product_id": course_id,
            "user_homework_id": user_homework_id,
            "question_record_id": question_record_id,
            "answers": answers
        }, headers={
            "x-referer": "https://scutspoc.xuetangx.com/lms#/" + course_id + "/" + class_id + "/homeworkList" +
                         "/homework/" + homework_id,
            "Referer": "https://scutspoc.xuetangx.com/lms",
            "Origin": "https://scutspoc.xuetangx.com"
        })
        return await r.json()

    async def homework_submit(self, course_id: str, class_id: str, homework_id, user_homework_id: int):
        r = await self.client.post("/inner_api/homework/submit/", {
            "class_id": class_id,
            "product_id": course_id,
            "user_homework_id": user_homework_id
        }, headers={
            "x-referer": "https://scutspoc.xuetangx.com/lms#/" + course_id + "/" + class_id + "/homeworkList" +
                         "/homework/" + homework_id,
            "Referer": "https://scutspoc.xuetangx.com/lms",
            "Origin": "https://scutspoc.xuetangx.com"
        })
        return await r.json()


class Heartbeat:
    url = None
    client = None
    headers = None

    i = 5
    et = None  # 事件类型
    p = "web"
    n = "sjy"  # group
    lob = "cloud3"
    cp = 0  # 当前时间
    fp = 0  # 跳转前时间(seeking事件)
    tp = 0  # 跳转后时间(seeking事件)
    sp = 1  # 播放速度
    ts = int(round(time.time() * 1000))  # 时间戳
    u = None  # 用户id(user_id)
    c = None  # 课程id(course_id)
    v = None  # 视频id(course_id)
    cc = None  # ? (=v)
    d = 0  # 视频总长度
    pg = None  # ? 视频id_????(意义不明，会变动)
    sq = 0  # 数据包序列
    t = "video"

    def __init__(self, url, headers, cookies, user_id, course_id, class_id, unit_id, video_id, duration, group):
        self.url = url
        self.client = httputils.Client(headers, cookies)
        self.u = user_id
        self.c = course_id
        self.v = video_id
        self.cc = video_id
        self.d = duration
        self.n = group
        self.pg = str(video_id) + "_" + ''.join(random.sample(string.ascii_letters + string.digits, 4))
        self.headers = {
            "x-referer": "https://scutspoc.xuetangx.com/lms#/" + course_id + "/" + class_id + "/"
                         + unit_id + "/" + video_id + "/0/handouts"
        }

    async def close(self):
        await self.client.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self):
        await self.client.close()

    async def send(self):
        self.sq = self.sq + 1
        r = await self.client.get(self.url, {
            "i": self.i,
            "et": self.et,
            "p": self.p,
            "n": self.n,
            "lob": self.lob,
            "cp": self.cp,
            "fp": self.fp,
            "tp": self.tp,
            "sp": self.sp,
            "ts": self.ts,
            "u": self.u,
            "c": self.c,
            "v": self.v,
            "cc": self.cc,
            "d": self.d,
            "pg": self.pg,
            "sq": self.sq,
            "t": self.t
        }, headers=self.headers)
        r = await r.json()
        return r

    def loadstart(self):
        self.et = "loadstart"
        return self.send()

    def loadeddata(self):
        self.et = "loadeddata"
        return self.send()

    def play(self):
        self.et = "play"
        return self.send()

    def playing(self):
        self.et = "playing"
        return self.send()

    def seeking(self, tp):
        self.et = "seeking"
        self.fp = self.cp
        self.tp = tp
        self.cp = tp
        return self.send()

    def ratechange(self, sp):
        self.et = "ratechange"
        self.sp = sp
        return self.send()

    def heartbeat(self):
        self.et = "heartbeat"
        return self.send()

    def pause(self):
        self.et = "pause"
        return self.send()

    def videoend(self):
        self.et = "videoend"
        return self.send()

    def set_to_end(self):
        self.time_add(self.d - self.cp)

    def time_add(self, t):
        self.cp = self.cp + t
        self.ts = self.ts + t * 1000
