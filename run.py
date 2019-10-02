import asyncio
import config
import api

cfg = config.load()

# if not config.cookies:
#     if api.login(input("Username: "), input("Password: ")) == 200:
#         config.save()
#     else:
#         print("Login failed")
#         exit()


API = api.API(cfg["headers"]["api"], cfg["cookies"])

info = {}


async def get_user_info():
    r = await API.header_ajax()
    global info
    info["user_id"] = str(r["userInfo"]["user_id"])  # 用户id
    info["real_name"] = str(r["userInfo"]["real_name"])  # 真实姓名
    info["user_number"] = str(r["userInfo"]["user_number"])  # 学号
    info["plat_id"] = str(r["plat_id"])  # 平台id


async def get_term():
    r = await API.plat_term(info["plat_id"])
    info["term_id_list"] = []
    for t in r["data"]:
        if t["term_id"] <= 0:
            continue
        info["term_id_list"].append(str(t["term_id"]))  # 学期id
        if t["is_current"]:
            info["term_id"] = str(t["term_id"])  # 当前学期id


async def get_course():
    r = await API.mycourse_list(info["term_id"])
    info["course_list"] = []
    for t in r["data"]["results"]:
        if t["status"] != "ing":
            continue
        info["course_list"].append({
            "class_id": str(t["class_id"]),  # 班级id
            "class_name": str(t["class_name"]),  # 班级名
            "course_id": str(t["course_id"]),  # 课程id
            "course_name": str(t["course_name"])  # 课程名
        })


# async def get_score(course):
#     r = await API.score(course["course_id"], course["class_id"])
#     course["video_list"] = []
#     for t in r["data"]["video"]["videos"]:
#         if t["visible"] is False or t["percent"] == 100:
#             continue
#         course["video_list"].append(t["item_id"])


async def get_courseware(course):
    r = await API.courseware(course["course_id"], course["class_id"])
    course["unit_list"] = []
    for t in r["data"]:
        if t["visible"] is False:
            continue
        course["unit_list"].append(t)


async def watch_course_video(course):
    print(course["course_name"], course["class_name"])
    for u in course["unit_list"]:
        for v in u["videosRecord"]["all"]:
            if v in u["videosRecord"]["done"]:
                continue
            print(u["unit_name"], u["unit_id"], v)
            r = await API.class_videos(course["course_id"], course["class_id"], u["unit_id"], v)
            hb = api.Heartbeat(cfg["url"]["heartbeat"], cfg["headers"]["heartbeat"], cfg["cookies"],
                               info["user_id"], course["course_id"], course["class_id"], u["unit_id"], v,
                               r["duration"], r["video_playurl"]["group"])
            # r = await API.get_video_watched_record(course["course_id"], course["class_id"], u["unit_id"], v)
            # r[v]
            # API.study_record()
            await hb.loadstart()
            await hb.loadeddata()
            await hb.play()
            await hb.playing()
            while hb.cp < hb.d:
                await hb.heartbeat()
                hb.time_add(5)
            # hb.set_to_end()
            await hb.heartbeat()
            await hb.pause()
            await hb.videoend()

            await hb.close()


async def main():
    await get_user_info()
    print("get_user_info:", info)
    await get_term()
    print("get_term:", info)
    await get_course()
    print("get_course:", info)
    for c in info["course_list"]:
        print("==========================================================")
        print(c)
        await get_courseware(c)
        print("get_courseware:", c)
        await watch_course_video(c)
        print("watch_course_video:", c)
    await API.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

# print("CourseIDs:")
# course_ids = []
# for term in api.filter_not_empty_terms()["list"]:
#     for course in api.studentcourse(term["id"])["results"]:
#         course_ids.append(course["course_id"])
#         print(course["course_id"])
# cid = course_ids[int(input("Select course:"))]
# li = api.courseware(cid)
# print(li)
# for chapter_hash in li.keys():
#     for sub_hash in li[chapter_hash]:
#         try:
#             print("page=", chapter_hash + "/" + sub_hash)
#             info = api.course(cid, chapter_hash, sub_hash)
#             if not info:
#                 continue
#             print(info)
#             ev = api.Event(info["video_id"], cid, chapter_hash, sub_hash)
#             hb = api.Heartbeat(cid, info["video_id"], info["ccsource"], 1200, ev.page)
#             # for url in info["problem_urls"]:
#             #     print(api.problem_show(url, {"host": "scut.xuetangx.com", "origin": "http://scut.xuetangx.com",
#             #                                  "referer": ev.page}))
#             # sources = api.videoid2source(info["ccsource"])["sources"]
#             # print(sources)
#             # ev.cdn_perf(sources["group"])
#             ev.load_video()
#             ev.play_video()
#             print("hb.play", hb.play().text)
#             while hb.cp < hb.d:
#                 print("hb.heartbeat", hb.heartbeat().text)
#             print("hb.pause", hb.pause().text)
#             print("hb.videoend", hb.videoend().text)
#             api.save_user_state(info["save-state-url"], "00:00:00")
#             ev.pause_video(1200)
#             ev.stop_video(1200)
#         except Exception as e:
#             print("Exception:", e)
#
#
# hb = api.Heartbeat(8761, 63929, 63929, 1200, "https://scutspoc.xuetangx.com/lms")
# for url in info["problem_urls"]:
#     print(api.problem_show(url, {"host": "scut.xuetangx.com", "origin": "http://scut.xuetangx.com",
#                                  "referer": ev.page}))
# sources = api.videoid2source(info["ccsource"])["sources"]
# print(sources)
# ev.cdn_perf(sources["group"])
# print("hb.play", hb.play().text)
# while hb.cp < hb.d:
#     print("hb.heartbeat", hb.heartbeat().text)
# print("hb.pause", hb.pause().text)
# print("hb.videoend", hb.videoend().text)
