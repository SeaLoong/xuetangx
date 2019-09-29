import httputils
import json
import re
import time
from bs4 import BeautifulSoup
import config


def login(username, password, remember=1):
    data = {"username": username, "password": password, "remember": remember}
    return httputils.post("http://scut.xuetangx.com/newcloud/api/v1/user/login/", data).status_code


def filter_manager_terms():
    return httputils.get("http://scut.xuetangx.com/newcloud/api/filter/manager/terms/").json()


def filter_not_empty_terms():
    return httputils.get("http://scut.xuetangx.com/newcloud/api/filter/not-empty-terms/", {"credit": 1}).json()


def header_ajax():
    return httputils.get("https://scutspoc.xuetangx.com/header_ajax").json()


def studentcourse(termid):
    return httputils.get("http://scut.xuetangx.com/newcloud/api/studentcourse/",
                         {"termid": termid, "search": "", "credit": 1, "status": "", "limit": 10, "page": 1}).json()


def courseware(course_id):
    r = httputils.get("http://scut.xuetangx.com/courses/" + course_id + "/courseware/")
    soup = BeautifulSoup(r.text, "html.parser")
    course_id = course_id.replace("+", "\+")
    reg = re.compile("/courses/" + course_id + "/courseware/(.+?)/(.+?)/")
    ret = {}
    for ele in soup.find_all("a"):
        ser = reg.search(ele["href"])
        if ser:
            if ret.get(ser.group(1)) is None:
                ret[ser.group(1)] = []
            ret[ser.group(1)].append(ser.group(2))
    return ret


def course(course_id, chapter_hash, sub_hash):
    r = httputils.get(
        "http://scut.xuetangx.com/courses/" + course_id + "/courseware/" + chapter_hash + "/" + sub_hash + "/")
    ret = {}
    try:
        ret = {
            "ccsource": re.search("ccsource=&#39;(.+?)&#39;", r.text).group(1),
            "save-state-url": "http://scut.xuetangx.com" + re.search("save-state-url=&#34;(.+?)&#34;", r.text).group(1),
            "video_id": re.search("v: &#39;(.+?)&#39;", r.text).group(1),
            "problem_urls": []
        }
        for m in re.findall("data-url=&#34;(.+?)&#34;", r.text):
            ret["problem_urls"].append("http://scut.xuetangx.com" + m)
    except AttributeError:
        pass
    return ret


def videoid2source(ccsource):
    return httputils.get("http://scut.xuetangx.com/videoid2source/" + ccsource).json()


def save_user_state(url, saved_video_position):
    return httputils.post(url, {"saved_video_position": saved_video_position}).json()


def problem_show(url, headers=None):
    return httputils.post(url + "/problem_show", headers=headers).json()


class Event:
    url = "http://scut.xuetangx.com/event"
    page = None
    video_id = None
    course_id = None
    headers = None

    def __init__(self, video_id, course_id, chapter_hash, sub_hash):
        self.video_id = video_id
        self.course_id = course_id
        self.page = "http://scut.xuetangx.com/courses/" + course_id + "/courseware/" + chapter_hash + "/" + sub_hash + "/"
        self.headers = {"host": "scut.xuetangx.com", "origin": "http://scut.xuetangx.com", "referer": self.page}

    def cdn_perf(self, expgroup):
        event = {"event": "load", "id": self.video_id, "expgroup": expgroup, "value": "",
                 "page": 0, "count": 1}
        data = {"event_type": "cdn_perf", "page": self.page, "event": json.dumps(event)}
        return httputils.post(self.url, data, headers=self.headers)

    def load_video(self):
        event = {"id": self.video_id, "code": "html5", "currentTime": 0, "cid": self.course_id}
        data = {"event_type": "load_video", "page": self.page, "event": json.dumps(event)}
        return httputils.post(self.url, data, headers=self.headers)

    def play_video(self):
        event = {"id": self.video_id, "code": "html5", "currentTime": 0, "cid": self.course_id}
        data = {"event_type": "play_video", "page": self.page, "event": json.dumps(event)}
        return httputils.post(self.url, data, headers=self.headers)

    def pause_video(self, currenttime):
        event = {"id": self.video_id, "code": "html5", "currentTime": currenttime, "cid": self.course_id}
        data = {"event_type": "pause_video", "page": self.page, "event": json.dumps(event)}
        return httputils.post(self.url, data, headers=self.headers)

    def stop_video(self, currenttime):
        event = {"id": self.video_id, "code": "html5", "currentTime": currenttime, "cid": self.course_id}
        data = {"event_type": "stop_video", "page": self.page, "event": json.dumps(event)}
        return httputils.post(self.url, data, headers=self.headers)


class Heartbeat:
    referer = None
    url = "http://scutspoc.xuetangx.com/heartbeat"
    i = 5
    et = "play"
    p = "web"
    cp = 0
    fp = 0
    tp = 0
    sp = 1
    ts = 0
    u = None
    c = None
    v = None
    cc = None
    d = 0
    pg = None
    sq = 1
    t = "video"

    def __init__(self, course_id, video_id, ccsource, d, referer):
        self.u = 665424
        self.c = course_id
        self.v = video_id
        self.cc = ccsource
        self.d = d
        self.pg = str(video_id) + "_10skt"
        self.referer = referer

    def send(self, ts=None):
        if ts is None:
            self.ts = int(round(time.time() * 1000))
        self.sq = self.sq + 1
        return httputils.get(self.url,
                             {"i": self.i, "et": self.et, "p": self.p, "cp": self.cp, "fp": self.fp, "tp": self.tp,
                              "sp": self.sp,
                              "ts": self.ts, "u": self.u, "c": self.c, "v": self.v, "cc": self.cc, "d": self.d,
                              "pg": self.pg,
                              "sq": self.sq, "t": self.t, "_": self.ts},
                             headers={"host": "scutspoc.xuetangx.com", "referer": self.referer})

    def play(self):
        self.et = "play"
        return self.send()

    def heartbeat(self):
        self.et = "heartbeat"
        self.cp = self.cp + 1200
        if self.cp > self.d:
            self.cp = self.d
        return self.send(self.ts + 1200000)

    def pause(self):
        self.et = "pause"
        self.cp = self.d
        return self.send()

    def videoend(self):
        self.et = "videoend"
        self.cp = self.d
        return self.send()
