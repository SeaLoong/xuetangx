import asyncio
import config
import api
import progressbar

cfg = config.load()
cookies = config.read_cookies()


API = None

info = None


async def get_user_info():
    r = await API.header_ajax()
    global info
    if r["islogin"] == 0:
        return False
    info["user_id"] = str(r["userInfo"]["user_id"])  # 用户id
    info["real_name"] = str(r["userInfo"]["real_name"])  # 真实姓名
    info["user_number"] = str(r["userInfo"]["user_number"])  # 学号
    info["plat_id"] = str(r["plat_id"])  # 平台id
    return True


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
    print("watching:", course["course_name"], course["class_name"])
    for u in course["unit_list"]:
        for v in u["videosRecord"]["all"]:
            if v in u["videosRecord"]["done"]:
                continue
            print(u["unit_name"], u["unit_id"], v)
            r = await API.class_videos(course["course_id"], course["class_id"], u["unit_id"], v)
            hb = api.Heartbeat(cfg["url"]["heartbeat"], cfg["headers"]["heartbeat"], info["cookies"],
                               info["user_id"], course["course_id"], course["class_id"], u["unit_id"], v,
                               r["duration"], r["video_playurl"]["group"])
            # r = await API.get_video_watched_record(course["course_id"], course["class_id"], u["unit_id"], v)
            # r[v]
            # API.study_record()
            await hb.loadstart()
            await hb.loadeddata()
            await hb.play()
            await hb.playing()
            bar = progressbar.ProgressBar(maxval=hb.d, widgets=[
                ' [', progressbar.Timer(), '] ',
                ' ', progressbar.SimpleProgress(), ' ',
                ' ', progressbar.Percentage(), ' ',
            ])
            bar.start()
            while hb.cp < hb.d:
                await hb.heartbeat()
                bar.update(hb.cp)
                hb.time_add(5)
            bar.finish()
            # hb.set_to_end()
            await hb.heartbeat()
            await hb.pause()
            await hb.videoend()

            await hb.close()


async def do_course_homework(course):
    print("doing homework:", course["course_name"], course["class_name"])
    for u in course["unit_list"]:
        print(u["unit_name"], u["unit_id"], u["open_time"], u["end_time"])
        for v in u["homeworkRecord"]["all"]:
            if v in u["homeworkRecord"]["done"]:
                continue
            print(u["unit_name"], u["unit_id"], v)
            r = await API.homework_subject(course["course_id"], course["class_id"], v)
            print(r["data"]["name"], r["data"]["now"], v, r["data"]["paper_id"])
            user_homework_id = r["data"]["user_homework_id"]
            question_data = r["data"]["question_data"]
            r = await API.homework_result(course["course_id"], course["class_id"], v, r["data"]["paper_id"])
            for question in question_data:
                for ans in r["data"]["question_data"]:
                    if ans["stem"] == question["stem"]:
                        if question["answers"] != ans["correct_answer"]:
                            print(question["question_id"], question["question_record_id"], question["stem"])
                            print(ans["correct_answer"])
                            print(await API.homework_answer(course["course_id"], course["class_id"], v,
                                                            user_homework_id, question["question_record_id"],
                                                            ans["correct_answer"]))
                        break


async def main():
    global API, info, cookies
    for cks in cookies:
        if len(cks) == 0:
            continue
        API = api.API(cfg["headers"]["api"], cks)
        info = {"cookies": cks}
        print("================================================================================")
        if not (await get_user_info()):
            print("Invalid Cookies:", cks)
            print("================================================================================")
            await API.close()
            continue
        print("get_user_info:", info)
        print("================================================================================")
        await get_term()
        print("get_term:", info)
        print("================================================================================")
        await get_course()
        print("get_course:", info)
        print("================================================================================")
        for c in info["course_list"]:
            print("================================================================================")
            print(c)
            await get_courseware(c)
            print("get_courseware:", c)
            print("================================================================================")
            print("watch_course_video")
            await watch_course_video(c)
            print("================================================================================")
            print("do_course_homework")
            await do_course_homework(c)
            print("================================================================================")
        await API.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
