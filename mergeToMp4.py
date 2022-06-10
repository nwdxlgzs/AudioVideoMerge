import os
'''
使用说明

文件结构：
        D:\\output
            |原神过场动画合集
                |视频介绍dir
                    |XXX（视频）.m2v
                    |XXX（音频）.wav
视频介绍dir与XXX一样时文件是：XXX.mp4
视频介绍dir与XXX不一样时文件是：视频介绍dir-XXX.mp4
'''
def mergeToMp4(m2v, wav, mp4):#合并视频和音频
    #清理文件
    if(os.path.exists(mp4)):
        print("文件已存在："+mp4)
        if(os.path.getsize(mp4) < 1024*1024*10):
            os.remove(mp4)
        else:
            return
    if(os.path.exists(m2v+".mp4")):
        os.remove(m2v+".mp4")
    if(os.path.exists(wav+".mp3")):
        os.remove(wav+".mp3")
    #先重编码再合并(目前是20mbps视频，2mbps音频)
    os.system(f"ffmpeg.exe -i {m2v} -c copy -vcodec h264 -preset placebo -b:v 20000k -an {m2v}.mp4")
    os.system(f"ffmpeg -i {wav} -f mp3 -ab 2000k {wav}.mp3")
    os.system(f"ffmpeg.exe -i {m2v}.mp4 -i {wav}.mp3 -vcodec copy -acodec copy {mp4}")
    #删除临时文件
    os.remove(m2v+".mp4")
    os.remove(wav+".mp3")


def getBindGroup(dir):#获取绑定组
    dirName = dir.split("\\")[-1]
    ls = []
    for fileName in os.listdir(dir):
        file = os.path.join(dir, fileName)
        if file.endswith("（视频）.m2v"):
            curName = fileName.split("（视频）")[0]
            if(curName == dirName):
                ls.append((file, file.replace("（视频）.m2v", "（音频）.wav"),
                          file.replace("（视频）.m2v", ".mp4")))
            else:
                ls.append((file, file.replace("（视频）.m2v", "（音频）.wav"),
                          os.path.join(dir, dirName+"-"+curName+".mp4")))

    return ls


def scanRootDir(dir):#扫描根目录
    ls = []
    for subdirName in os.listdir(dir):
        subdir = os.path.join(dir, subdirName)
        ls.append(subdir)
    return ls


rootLS = scanRootDir("D:\\output\\原神过场动画合集")
for root in rootLS:
    ls = getBindGroup(root)
    for item in ls:
        print(item)
        mergeToMp4(item[0], item[1], item[2])

print("done")
