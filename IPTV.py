import os

#функция поиска необходимых файлов
def func_search(x,y) :
	result = os.listdir("./")
	for file in result :
		if file.endswith(x) :
			y.append(file)



#поиск видеофайлов в директоории
ts = []
func_search(".ts",ts)



#поиск ошибок с помощи ffmpeg
for i in ts :
	command = 'ffmpeg -v error -i ' + i + ' -map 0:1 -f null - 2>' + i +'.log'
	os.system(command)



#поиск логов в директории
log = []
func_search(".log",log)



#поиск ошибок в логах
StrError = ('Error while decoding stream '+ chr(35) +'0:1: Invalid data found when processing input' + '\n')
Final_log = open('Final_log.txt','w')

for i in log :
	open_file = open(i,'r')
	for j in open_file :
		Res = j == StrError
		if Res :
			Final_log.write(i +' = Fail' + '\n')
			break
	if not Res:
		Final_log.write(i +' = Ok' + '\n')
Final_log.close()



#вывод результатов на экран
print_Final_log = open('Final_log.txt','r')
print(print_Final_log.read())
