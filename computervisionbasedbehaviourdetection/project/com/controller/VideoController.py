import os
import time
from datetime import datetime, date

import cv2
import imutils
import numpy as np
from flask import request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.BranchDAO import BranchDAO
from project.com.dao.PackageDAO import PackageDAO
from project.com.dao.PurchaseDAO import PurchaseDAO
from project.com.dao.RegionFourDAO import RegionFourDAO
from project.com.dao.RegionOneDAO import RegionOneDAO
from project.com.dao.RegionThreeDAO import RegionThreeDAO
from project.com.dao.RegionTwoDAO import RegionTwoDAO
from project.com.dao.RestaurantDAO import RestaurantDAO
from project.com.dao.VideoDAO import VideoDAO
from project.com.vo.BranchVO import BranchVO
from project.com.vo.PurchaseVO import PurchaseVO
from project.com.vo.RegionFourVO import RegionFourVO
from project.com.vo.RegionOneVO import RegionOneVO
from project.com.vo.RegionThreeVO import RegionThreeVO
from project.com.vo.RegionTwoVO import RegionTwoVO
from project.com.vo.RestaurantVO import RestaurantVO
from project.com.vo.VideoVO import VideoVO

UPLOAD_FOLDER = 'project/static/userResources/video/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/user/loadVideo')
def userLoadVideo():
    try:
        if adminLoginSession() == 'user':
            purchaseDAO = PurchaseDAO()
            purchaseVO = PurchaseVO()
            purchase_LoginId = session.get('session_loginId')
            purchaseVO.purchase_LoginId = purchase_LoginId
            purchaseList = purchaseDAO.validatePurchase(purchaseVO)
            print(purchaseList)
            if len(purchaseList) != 0:
                branchDAO = BranchDAO()
                branchVO = BranchVO()
                restaurantDAO = RestaurantDAO()
                restaurantVO = RestaurantVO()

                restaurant_loginId = session['session_loginId']

                restaurantVO.restaurant_LoginId = restaurant_loginId
                restaurantVOList = restaurantDAO.viewRestaurant(restaurantVO)
                branchVO.branch_RestaurantId = restaurantVOList[0].restaurantId

                branchVOList = branchDAO.viewBranch(branchVO)
                return render_template('user/addDetection.html', branchVOList=branchVOList)
            else:
                packageDAO = PackageDAO()
                packageVOList = packageDAO.viewPackage()
                return render_template('user/addPurchase.html', packageVOList=packageVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertVideo', methods=['POST'])
def userInsertVideo():
    try:
        if adminLoginSession() == 'user':
            videoVO = VideoVO()
            videoDAO = VideoDAO()

            file = request.files['file']
            print(file)

            videoFileName = secure_filename(file.filename)
            print(videoFileName)

            videoFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            print(videoFilePath)

            videoUploadDate = str(date.today())
            print(videoUploadDate)

            videoUploadTime = str(datetime.now().strftime("%H:%M:%S"))
            print(videoUploadTime)

            video_BranchId = request.form['video_BranchId']
            video_LoginId = session.get('session_loginId')

            file.save(os.path.join(videoFilePath, videoFileName))

            branchVO = BranchVO()
            branchDAO = BranchDAO()

            branchVO.branchId = video_BranchId

            branchVOList = branchDAO.getAreaByBranch(branchVO)

            areaId = branchVOList[0].branch_AreaId

            videoVO.inputVideoFileName = videoFileName
            videoVO.inputVideoFilePath = videoFilePath.replace('project', '..')
            videoVO.inputVideoUploadDate = videoUploadDate
            videoVO.inputVideoUploadTime = videoUploadTime
            videoVO.video_BranchId = video_BranchId
            videoVO.video_AreaId = areaId
            videoVO.video_LoginId = video_LoginId

            inputVideo = r'{}/{}'.format(videoFilePath, videoFileName)

            outputVideoName = videoFileName.replace('.mp4', '.webm')

            outputVideo = r'project/static/userResources/video/output/{}'.format(outputVideoName)

            outputVideoPath = r'project/static/userResources/video/output/'

            model_dump = r'project/static/userResources/modelDump/yolo-coco'

            confidence_default = 0.5

            threshold = 0.5

            labelsPath = os.path.sep.join([model_dump, "coco.names"])

            LABELS = open(labelsPath).read().strip().split("\n")

            # initialize a list of colors to represent each possible class label
            np.random.seed(42)

            COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

            count = 0
            s1 = 0
            s2 = 0
            s3 = 0
            s4 = 0
            region1 = 0
            region2 = 0
            region3 = 0
            region4 = 0
            region1_frameCounter = 0
            region2_frameCounter = 0
            region3_frameCounter = 0
            region4_frameCounter = 0
            region1_non_frameCounter = 0
            region2_non_frameCounter = 0
            region3_non_frameCounter = 0
            region4_non_frameCounter = 0
            non_frameCounter = 0
            text = None
            x = 0
            y = 0
            color = (0, 0, 255)

            # derive the paths to the YOLO weights and model configuration
            weightsPath = os.path.sep.join([model_dump, "yolov3.weights"])
            configPath = os.path.sep.join([model_dump, "yolov3.cfg"])

            # load our YOLO object detector trained on COCO dataset (80 classes)
            # and determine only the *output* layer names that we need from YOLO
            print("[INFO] loading YOLO from disk...")
            net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
            ln = net.getLayerNames()
            ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

            # initialize the video stream, pointer to output video file, and
            # frame dimensions
            vs = cv2.VideoCapture(inputVideo)
            writer = None
            (W, H) = (None, None)

            # try to determine the total number of frames in the video file
            try:
                prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
                    else cv2.CAP_PROP_FRAME_COUNT
                total = int(vs.get(prop))
                print("[INFO] {} total frames in video".format(total))

            # an error occurred while trying to determine the total
            # number of frames in the video file
            except:
                print("[INFO] could not determine # of frames in video")
                print("[INFO] no approx. completion time can be provided")
                total = -1

            # loop over frames from the video file stream
            region1_time_list = []
            region1_person_list = []
            region1_person_list_avg = []
            region1_time_list_avg = []
            region_one_id_list = []

            region2_time_list = []
            region2_person_list = []
            region2_person_list_avg = []
            region2_time_list_avg = []
            region_two_id_list = []

            region3_time_list = []
            region3_person_list = []
            region3_person_list_avg = []
            region3_time_list_avg = []
            region_three_id_list = []

            region4_time_list = []
            region4_person_list = []
            region4_person_list_avg = []
            region4_time_list_avg = []
            region_four_id_list = []

            while True:
                # read the next frame from the file
                (grabbed, frame) = vs.read()

                # if the frame was not grabbed, then we have reached the end
                # of the stream
                if not grabbed:
                    break

                # if the frame dimensions are empty, grab them
                if W is None or H is None:
                    (H, W) = frame.shape[:2]

                # construct a blob from the input frame and then perform a forward
                # pass of the YOLO object detector, giving us our bounding boxes
                # and associated probabilities
                blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                             swapRB=True, crop=False)
                net.setInput(blob)
                start = time.time()
                layerOutputs = net.forward(ln)
                end = time.time()

                # initialize our lists of detected bounding boxes, confidences,
                # and class IDs, respectively
                boxes = []
                confidences = []
                classIDs = []

                if count % 10 == 0:
                    # loop over each of the layer outputs
                    for output in layerOutputs:

                        # loop over each of the detections
                        for detection in output:
                            # extract the class ID and confidence (i.e., probability)
                            # of the current object detection

                            scores = detection[5:]
                            classID = np.argmax(scores)
                            confidence = scores[classID]

                            # filter out weak predictions by ensuring the detected
                            # probability is greater than the minimum probability
                            if confidence > confidence_default:
                                # scale the bounding box coordinates back relative to
                                # the size of the image, keeping in mind that YOLO
                                # actually returns the center (x, y)-coordinates of
                                # the bounding box followed by the boxes' width and
                                # height
                                if LABELS[classID] != "person":
                                    continue

                                box = detection[0:4] * np.array([W, H, W, H])
                                (centerX, centerY, width, height) = box.astype("int")

                                # use the center (x, y)-coordinates to derive the top
                                # and and left corner of the bounding box
                                x = int(centerX - (width / 2))
                                y = int(centerY - (height / 2))

                                # update our list of bounding box coordinates,
                                # confidences, and class IDs
                                boxes.append([x, y, int(width), int(height)])
                                confidences.append(float(confidence))
                                classIDs.append(classID)

                    # apply non-maxima suppression to suppress weak, overlapping
                    # bounding boxes
                    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence_default,
                                            threshold)

                    # draw a horizontal line in the center of the frame -- once an
                    # object crosses this line we will determine whether they were
                    # moving 'up' or 'down'
                    # ensure at least one detection exists

                    # TODO add below points
                    # count the zero len of boxes == if zero count more than defined frame consider table not occupied
                    # avaerage the region count from predefined interval

                    if len(idxs) > 0:
                        region1 = 0
                        region2 = 0
                        region3 = 0
                        region4 = 0
                        # loop over the indexes we are keeping
                        for i in idxs.flatten():
                            # extract the bounding box coordinates
                            (x, y) = (boxes[i][0], boxes[i][1])
                            (w, h) = (boxes[i][2], boxes[i][3])

                            centerx = x + w // 2
                            centery = y + h // 2

                            if centerx < W // 2 and centery < H // 2:
                                region1 = region1 + 1
                                region1_frameCounter += 1
                                region1_non_frameCounter = 0
                                region1_person_list.append(region1)
                                region1_time_list.append((s1 // 3))
                                if region1_frameCounter > 20:
                                    # send to database
                                    print("store list in db 1")
                                    print("region1_person_list>>>>>>>>>", region1_person_list)
                                    print("region1_time_list>>>>>>>>", region1_time_list)

                            else:
                                region1_non_frameCounter += 1
                                if region1_non_frameCounter > 20:
                                    # send to database
                                    print("not occupied 1")

                            if centerx < W // 2 and centery > H // 2:
                                region2 = region2 + 1
                                region2_frameCounter += 1
                                region2_non_frameCounter = 0
                                region2_person_list.append(region2)
                                region2_time_list.append((s2 // 3))
                                if region2_frameCounter > 20:
                                    # send to database
                                    print("store list in db 2")
                                    print("region2_person_list>>>>>>>>>", region2_person_list)
                                    print("region2_time_list>>>>>>>>", region2_time_list)

                            else:
                                region2_non_frameCounter += 1
                                if region2_non_frameCounter > 20:
                                    # send to database
                                    print("not occupied 2")

                            if centerx > W // 2 and centery < H // 2:
                                region3 = region3 + 1
                                region3_frameCounter += 1
                                region3_non_frameCounter = 0
                                region3_person_list.append(region3)
                                region3_time_list.append((s3 // 3))
                                if region3_frameCounter > 20:
                                    # send to database
                                    print("store list in db 3")
                                    print("region3_person_list>>>>>>>>>", region3_person_list)
                                    print("region3_time_list>>>>>>>>", region3_time_list)

                            else:
                                region3_non_frameCounter += 1
                                if region3_non_frameCounter > 20:
                                    # send to database
                                    print("not occupied 3")

                            if centerx > W // 2 and centery > H // 2:
                                region4 = region4 + 1
                                region4_frameCounter += 1
                                region4_non_frameCounter = 0
                                region4_person_list.append(region4)
                                region4_time_list.append((s4 // 3))
                                if region4_frameCounter > 20:
                                    # send to database
                                    print("store list in db 4")
                                    print("region4_person_list>>>>>>>>>", region4_person_list)
                                    print("region4_time_list>>>>>>>>", region4_time_list)

                            else:
                                region4_non_frameCounter += 1
                                if region4_non_frameCounter > 20:
                                    # send to database
                                    print("not occupied 4")

                            # draw a bounding box rectangle and label on the frame
                            color = [int(c) for c in COLORS[classIDs[i]]]
                            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                            text = "{}: {:.4f}".format(LABELS[classIDs[i]],
                                                       confidences[i])

                        if region1 > 0:
                            s1 = s1 + 1
                        else:
                            s1 = 0
                            if len(region1_person_list) != 0:
                                freq = {}
                                counter = 0
                                list = []
                                for items in region1_person_list:
                                    freq[items] = region1_person_list.count(items)

                                for key, value in freq.items():
                                    print("% d : % d" % (key, value))
                                    counter += value
                                for key, value in freq.items():
                                    if (value / counter) * 100 > 15:
                                        print("% d : % d" % (key, value))
                                        list.append(key)
                                if max(region1_time_list) > 10:
                                    region1_person_list_avg.append(max(list))
                                    region1_time_list_avg.append(max(region1_time_list))
                            region1_person_list = []
                            region1_time_list = []
                        if region2 > 0:
                            s2 = s2 + 1
                        else:
                            s2 = 0
                            if len(region2_person_list) != 0:
                                freq = {}
                                counter = 0
                                list = []
                                for items in region2_person_list:
                                    freq[items] = region2_person_list.count(items)

                                for key, value in freq.items():
                                    print("% d : % d" % (key, value))
                                    counter += value
                                for key, value in freq.items():
                                    if (value / counter) * 100 > 15:
                                        print("% d : % d" % (key, value))
                                        list.append(key)
                                if max(region2_time_list) > 10:
                                    region2_person_list_avg.append(max(list))
                                    region2_time_list_avg.append(max(region2_time_list))
                            region2_person_list = []
                            region2_time_list = []
                        if region3 > 0:
                            s3 = s3 + 1
                        else:
                            s3 = 0
                            if len(region3_person_list) != 0:
                                freq = {}
                                counter = 0
                                list = []
                                for items in region3_person_list:
                                    freq[items] = region3_person_list.count(items)

                                for key, value in freq.items():
                                    print("% d : % d" % (key, value))
                                    counter += value
                                for key, value in freq.items():
                                    if (value / counter) * 100 > 15:
                                        print("% d : % d" % (key, value))
                                        list.append(key)
                                if max(region3_time_list) > 10:
                                    region3_person_list_avg.append(max(list))
                                    region3_time_list_avg.append(max(region3_time_list))
                            region3_person_list = []
                            region3_time_list = []
                        if region4 > 0:
                            s4 = s4 + 1
                        else:
                            s4 = 0
                            if len(region4_person_list) != 0:
                                freq = {}
                                counter = 0
                                list = []
                                for items in region4_person_list:
                                    freq[items] = region4_person_list.count(items)

                                for key, value in freq.items():
                                    print("% d : % d" % (key, value))
                                    counter += value
                                for key, value in freq.items():
                                    if (value / counter) * 100 > 15:
                                        print("% d : % d" % (key, value))
                                        list.append(key)
                                if max(region4_time_list) > 10:
                                    region4_person_list_avg.append(max(list))
                                    region4_time_list_avg.append(max(region4_time_list))
                            region4_person_list = []
                            region4_time_list = []

                    else:
                        non_frameCounter += 1
                        if non_frameCounter > 20:
                            print("No Person in frame !")
                            region1 = 0
                            region2 = 0
                            region3 = 0
                            region4 = 0
                            s1 = 0
                            s2 = 0
                            s3 = 0
                            s4 = 0

                cv2.line(frame, (0, H // 2), (W, H // 2), (0, 255, 255), 2)
                cv2.line(frame, (W // 2, 0), (W // 2, H), (0, 255, 255), 2)

                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                cv2.putText(frame, str(region1) + " " + str(s1 // 3), (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                            (0, 0, 255),
                            2)
                cv2.putText(frame, str(region2) + " " + str(s2 // 3), (0, H - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                            (0, 0, 255), 2)
                cv2.putText(frame, str(region3) + " " + str(s3 // 3), (W // 2 + 20, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75,
                            (0, 0, 255), 2)
                cv2.putText(frame, str(region4) + " " + str(s4 // 3), (W // 2 + 20, H - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                            (0, 0, 255), 2)

                count = count + 1

                # check if the video writer is None
                if writer is None:
                    # initialize our video writer
                    fourcc = cv2.VideoWriter_fourcc(*"VP80")
                    writer = cv2.VideoWriter(outputVideo, fourcc, 30,
                                             (frame.shape[1], frame.shape[0]), True)

                    # some information on processing single frame
                    if total > 0:
                        elap = (end - start)
                        print("[INFO] single frame took {:.4f} seconds".format(elap))
                        print("[INFO] estimated total time to finish: {:.4f}".format(
                            (elap * total) / 60))

                # write the output frame to disk
                # cv2.imshow("image",frame)
                writer.write(frame)

            print("region1personlist>>>>>>>>", region1_person_list)
            print("region1timelist>>>>>>>>", region1_time_list)
            print("region1personlistavg>>>>>>>>", region1_person_list_avg)
            print("region1timelistavg>>>>>>>>", region1_time_list_avg)
            if len(region1_person_list_avg) > 0:
                for i in range(len(region1_person_list_avg)):
                    regionOneVO = RegionOneVO()
                    regionOneDAO = RegionOneDAO()
                    regionOneVO.regionOnePerson = region1_person_list_avg[i]
                    regionOneVO.regionOneTime = region1_time_list_avg[i]
                    regionOneDAO.insertLogOne(regionOneVO)
                    region_one_id_list.append(regionOneVO.regionOneId)

            print("region2personlist>>>>>>>>", region2_person_list)
            print("region2timelist>>>>>>>>", region2_time_list)
            print("region2personlistavg>>>>>>>>", region2_person_list_avg)
            print("region2timelistavg>>>>>>>>", region2_time_list_avg)
            if len(region2_person_list_avg) > 0:
                for i in range(len(region2_person_list_avg)):
                    regionTwoVO = RegionTwoVO()
                    regionTwoDAO = RegionTwoDAO()
                    regionTwoVO.regionTwoPerson = region2_person_list_avg[i]
                    regionTwoVO.regionTwoTime = region2_time_list_avg[i]
                    regionTwoDAO.insertLogTwo(regionTwoVO)
                    region_two_id_list.append(regionTwoVO.regionTwoId)

            print("region3personlist>>>>>>>>", region3_person_list)
            print("region3timelist>>>>>>>>", region3_time_list)
            print("region3personlistavg>>>>>>>>", region3_person_list_avg)
            print("region3timelistavg>>>>>>>>", region3_time_list_avg)
            if len(region3_person_list_avg) > 0:
                for i in range(len(region3_person_list_avg)):
                    regionThreeVO = RegionThreeVO()
                    regionThreeDAO = RegionThreeDAO()
                    regionThreeVO.regionThreePerson = region3_person_list_avg[i]
                    regionThreeVO.regionThreeTime = region3_time_list_avg[i]
                    regionThreeDAO.insertLogThree(regionThreeVO)
                    region_three_id_list.append(regionThreeVO.regionThreeId)

            print("region4personlist>>>>>>>>", region4_person_list)
            print("region4timelist>>>>>>>>", region4_time_list)
            print("region4personlistavg>>>>>>>>", region4_person_list_avg)
            print("region4timelistavg>>>>>>>>", region4_time_list_avg)
            if len(region4_person_list_avg) > 0:
                for i in range(len(region4_person_list_avg)):
                    regionFourVO = RegionFourVO()
                    regionFourDAO = RegionFourDAO()
                    regionFourVO.regionFourPerson = region4_person_list_avg[i]
                    regionFourVO.regionFourTime = region4_time_list_avg[i]
                    regionFourDAO.insertLogFour(regionFourVO)
                    region_four_id_list.append(regionFourVO.regionFourId)

            # release the file pointers
            print("[INFO] cleaning up...")
            writer.release()
            vs.release()
            videoFileName = outputVideoName
            print(videoFileName)

            videoFilePath = outputVideoPath
            print(videoFilePath)

            videoUploadDate = str(date.today())
            print(videoUploadDate)

            videoUploadTime = str(datetime.now().strftime("%H:%M:%S"))
            print(videoUploadTime)

            videoVO.outputVideoFileName = videoFileName
            videoVO.outputVideoFilePath = videoFilePath.replace('project', '..')
            videoVO.outputVideoUploadDate = videoUploadDate
            videoVO.outputVideoUploadTime = videoUploadTime

            videoDAO.insertVideo(videoVO)

            if len(region_one_id_list) > 0:
                for i in region_one_id_list:
                    regionOneVO = RegionOneVO()
                    regionOneDAO = RegionOneDAO()
                    regionOneVO.regionOne_VideoId = videoVO.videoId
                    regionOneVO.regionOneId = i
                    regionOneDAO.updateRegionOne(regionOneVO)

            if len(region_two_id_list) > 0:
                for i in region_two_id_list:
                    regionTwoVO = RegionTwoVO()
                    regionTwoDAO = RegionTwoDAO()
                    regionTwoVO.regionTwo_VideoId = videoVO.videoId
                    regionTwoVO.regionTwoId = i
                    regionTwoDAO.updateRegionTwo(regionTwoVO)

            if len(region_three_id_list) > 0:
                for i in region_three_id_list:
                    regionThreeVO = RegionThreeVO()
                    regionThreeDAO = RegionThreeDAO()
                    regionThreeVO.regionThree_VideoId = videoVO.videoId
                    regionThreeVO.regionThreeId = i
                    regionThreeDAO.updateRegionThree(regionThreeVO)

            if len(region_four_id_list) > 0:
                for i in region_four_id_list:
                    regionFourVO = RegionFourVO()
                    regionFourDAO = RegionFourDAO()
                    regionFourVO.regionFour_VideoId = videoVO.videoId
                    regionFourVO.regionFourId = i
                    regionFourDAO.updateRegionFour(regionFourVO)

            return redirect(url_for('userViewVideo'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewVideo', methods=['GET'])
def userViewVideo():
    try:
        if adminLoginSession() == 'user':
            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()
            videoDAO = VideoDAO()
            videoVO = VideoVO()
            video_LoginId = session.get('session_loginId')
            videoVO.video_LoginId = video_LoginId
            videoVOList = videoDAO.viewVideo(videoVO)

            return render_template('user/viewDetection.html', videoVOList=videoVOList, areaVOList=areaVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deleteVideo', methods=['GET'])
def userDeleteVideo():
    try:
        if adminLoginSession() == 'user':
            videoVO = VideoVO()

            videoDAO = VideoDAO()

            videoId = request.args.get('videoId')

            regionOneVO = RegionOneVO()
            regionOneDAO = RegionOneDAO()
            regionOneVO.regionOne_VideoId = videoId
            regionOneList = regionOneDAO.findRegionOneByVideoId(regionOneVO)
            if len(regionOneList) != 0:
                regionOneVO.regionOneId = regionOneList[0].regionOneId
                regionOneDAO.deleteRegionOne(regionOneVO)

            regionTwoVO = RegionTwoVO()
            regionTwoDAO = RegionTwoDAO()
            regionTwoVO.regionTwo_VideoId = videoId
            regionTwoList = regionTwoDAO.findRegionTwoByVideoId(regionTwoVO)
            if len(regionTwoList) != 0:
                regionTwoVO.regionTwoId = regionTwoList[0].regionTwoId
                regionTwoDAO.deleteRegionTwo(regionTwoVO)

            regionThreeVO = RegionThreeVO()
            regionThreeDAO = RegionThreeDAO()
            regionThreeVO.regionThree_VideoId = videoId
            regionThreeList = regionThreeDAO.findRegionThreeByVideoId(regionThreeVO)
            if len(regionThreeList) != 0:
                regionThreeVO.regionThreeId = regionThreeList[0].regionThreeId
                regionThreeDAO.deleteRegionThree(regionThreeVO)

            regionFourVO = RegionFourVO()
            regionFourDAO = RegionFourDAO()
            regionFourVO.regionFour_VideoId = videoId
            regionFourList = regionFourDAO.findRegionFourByVideoId(regionFourVO)
            if len(regionFourList) != 0:
                regionFourVO.regionFourId = regionFourList[0].regionFourId
                regionFourDAO.deleteRegionFour(regionFourVO)


            videoVO.videoId = videoId

            videoList = videoDAO.deleteVideo(videoVO)

            print(videoList)

            videoFilename = videoList.inputVideoFileName
            videoFilepath = videoList.inputVideoFilePath.replace('..', 'project')
            outputVideoFilename = videoList.outputVideoFileName
            outputVideoFilepath = videoList.outputVideoFilePath.replace('..', 'project')

            inputPath = videoFilepath + videoFilename
            outputPath = outputVideoFilepath + outputVideoFilename

            os.remove(inputPath)
            os.remove(outputPath)

            return redirect(url_for('userViewVideo'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewDetails', methods=['GET'])
def userViewDetails():
    try:
        if adminLoginSession() == 'user':
            videoVO = VideoVO()

            videoDAO = VideoDAO()

            videoId = request.args.get('videoId')

            videoVO.videoId = videoId

            regionDetailList = []

            regionOneVO = RegionOneVO()
            regionOneDAO = RegionOneDAO()
            regionOneVO.regionOne_VideoId = videoVO.videoId
            regionOneVOList = regionOneDAO.regionOnePersonCount(regionOneVO)
            regionOneCount = regionOneVOList.regionOnePersonCount
            regionDetailList.append(regionOneCount)
            regionOneList = regionOneDAO.regionOneTimeCount(regionOneVO)
            regionOneTime = regionOneList.regionOneTimeCount
            regionDetailList.append(regionOneTime)
            print('regionOneCount>>>>>>>>', regionOneVOList.regionOnePersonCount)

            regionTwoVO = RegionTwoVO()
            regionTwoDAO = RegionTwoDAO()
            regionTwoVO.regionTwo_VideoId = videoVO.videoId
            regionTwoVOList = regionTwoDAO.regionTwoPersonCount(regionTwoVO)
            regionTwoCount = regionTwoVOList.regionTwoPersonCount
            regionDetailList.append(regionTwoCount)
            regionTwoList = regionTwoDAO.regionTwoTimeCount(regionTwoVO)
            regionTwoTime = regionTwoList.regionTwoTimeCount
            regionDetailList.append(regionTwoTime)
            print('regionTwoCount>>>>>>>>', regionTwoVOList.regionTwoPersonCount)

            regionThreeVO = RegionThreeVO()
            regionThreeDAO = RegionThreeDAO()
            regionThreeVO.regionThree_VideoId = videoVO.videoId
            regionThreeVOList = regionThreeDAO.regionThreePersonCount(regionThreeVO)
            regionThreeCount = regionThreeVOList.regionThreePersonCount
            regionDetailList.append(regionThreeCount)
            regionThreeList = regionThreeDAO.regionThreeTimeCount(regionThreeVO)
            regionThreeTime = regionThreeList.regionThreeTimeCount
            regionDetailList.append(regionThreeTime)
            print('regionThreeCount>>>>>>>>', regionThreeVOList.regionThreePersonCount)

            regionFourVO = RegionFourVO()
            regionFourDAO = RegionFourDAO()
            regionFourVO.regionFour_VideoId = videoVO.videoId
            regionFourVOList = regionFourDAO.regionFourPersonCount(regionFourVO)
            regionFourCount = regionFourVOList.regionFourPersonCount
            regionDetailList.append(regionFourCount)
            regionFourList = regionFourDAO.regionFourTimeCount(regionFourVO)
            regionFourTime = regionFourList.regionFourTimeCount
            regionDetailList.append(regionFourTime)
            print('regionFourCount>>>>>>>>', regionFourVOList.regionFourPersonCount)

            return render_template('user/viewDetails.html', regionDetailList=regionDetailList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewVideo', methods=['GET'])
def adminViewVideo():
    try:
        if adminLoginSession() == 'admin':
            videoDAO = VideoDAO()
            videoVOList = videoDAO.adminViewVideo()

            return render_template('admin/viewDetection.html', videoVOList=videoVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewVideoByArea', methods=['GET'])
def userViewVideoByArea():
    try:
        if adminLoginSession() == 'user':
            areaId = request.args.get('areaId')
            videoDAO = VideoDAO()
            videoVO = VideoVO()
            video_LoginId = session.get('session_loginId')
            videoVO.video_AreaId = areaId
            videoVO.video_LoginId = video_LoginId
            videoVOList = videoDAO.viewVideoByArea(videoVO)
            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()
            return render_template('user/viewDetection.html', videoVOList=videoVOList, areaVOList=areaVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
