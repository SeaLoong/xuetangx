import config
import api
import httputils

config.load()


# if not config.cookies:
#     if api.login(input("Username: "), input("Password: ")) == 200:
#         config.save()
#     else:
#         print("Login failed")
#         exit()
#
httputils.init()
#
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


hb = api.Heartbeat(8761, 63929, 63929, 1200, "https://scutspoc.xuetangx.com/lms")
# for url in info["problem_urls"]:
#     print(api.problem_show(url, {"host": "scut.xuetangx.com", "origin": "http://scut.xuetangx.com",
#                                  "referer": ev.page}))
# sources = api.videoid2source(info["ccsource"])["sources"]
# print(sources)
# ev.cdn_perf(sources["group"])
print("hb.play", hb.play().text)
while hb.cp < hb.d:
    print("hb.heartbeat", hb.heartbeat().text)
print("hb.pause", hb.pause().text)
print("hb.videoend", hb.videoend().text)
