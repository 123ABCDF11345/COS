# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
import tkinter.filedialog
import tkinter.messagebox
import tkinter
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
print("初始化中.........在此之前，感谢您打开电脑运行我这个lj程序，有问题就反馈，好吗？---汪俊择  对了，你得先联网才能用")
secret_id = 'AKIDBAdsvmG5tZ1xfCBckpjOny3tT3bz34Zt'
secret_key = 'EQN0R6VfiW3SjphW6Xs9F2fyGNOqjSks'
region = 'ap-guangzhou'
token = None
scheme = 'https' 
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)
def UpFill():
	OnName=input("请输入上传文件的名称（需要后缀名）：     ")
	root=tkinter.Tk()
	Fillname=tkinter.filedialog.askopenfilename()
	FillHome=Fillname
	root.destroy()
	try:
		with open(FillHome, 'rb') as fp:
		    response = client.put_object(
		        Bucket='gao-ta-1300361781',
		        Body=fp,
		        Key=OnName,
		        StorageClass='STANDARD',
		        EnableMD5=False
		    )
	except FileNotFoundError:
		root=tkinter.Tk()
		tkinter.messagebox.showerror('错误','没有找到指定文件，请重试')
		root.destroy()
		Root()
	except:
		root=tkinter.Tk()
		tkinter.messagebox.showerror('错误','未知的错误，请检查网络后重试，如仍然报错，请上报至2542594900@qq.com')
		root.destroy()
		Root()
	root=tkinter.Tk()
	tkinter.messagebox.showinfo('上传','选定项目上传完成')
	root.destroy()
def ListFill():
	response = client.list_objects(Bucket='gao-ta-1300361781')
	#print(response)
	try:
		response1=response['Contents']
	except KeyError:
		root=tkinter.Tk()
		tkinter.messagebox.showerror('错误','当前网盘中暂无文件')
		root.destroy()
		Root()
	for each_list in response1:  
		print(each_list["Key"])
def DownFill():
	OnName=input("请输入在网盘上的名称（需要后缀名）：       ")
	response = client.get_object(
    Bucket='gao-ta-1300361781',
    Key=OnName)
	response['Body'].get_stream_to_file(OnName)
	root=tkinter.Tk()
	tkinter.messagebox.showinfo('下载','选定项目下载完成')
	root.destroy()
def Boom():
	OnName=input("请输入在网盘上的名称（需要后缀名） 提示：如输入错误名称，将无报错：     ")
	response = client.delete_object(
    Bucket='gao-ta-1300361781',
    Key=OnName)
	#print(response)
	root=tkinter.Tk()
	tkinter.messagebox.showinfo('删除','选定项目删除完成')
	root.destroy()
def Root():
	try:
		O=input("上传or遍历or下载or删除or关于软件（直接输入想要执行的对象）：      ")
		if O=="上传":
			UpFill()
		elif O=="遍历":
			ListFill()
		elif O=="下载":
			print("当前云端所有文件：  ")
			ListFill()
			DownFill()
		elif O=="删除":
			print("当前云端所有文件：  ")
			ListFill()
			Boom()
		elif O=="关于软件":
			root=tkinter.Tk()
			tkinter.messagebox.showinfo('关于软件','本软件由汪俊择开发，依据腾讯云COS服务部署，总存储容量50GB，容灾0GB，标准写入模式，并发量5包/s 注意：本网盘不承担资料保存服务丢失的责任！')
			root.destroy()
	except qcloud_cos.cos_exception.CosClientError:
		root=tkinter.Tk()
		tkinter.messagebox.showinfo('错误','无法连接到线上COS，请检查网络')
		root.destroy()
	else:
		Root()
Root()