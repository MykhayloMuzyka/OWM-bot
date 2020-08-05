import speedtest

test = speedtest.Speedtest()
download = test.download()
upload = test.upload()

print(f"Download speed: {(download/1024)/1024} Mb/s \nUpload Speed : {(upload/1024)/1024} Mb/s")