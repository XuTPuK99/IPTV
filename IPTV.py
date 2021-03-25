import os

#������� ������ ����������� ������
def func_search(x,y) :
	result = os.listdir("./")
	for file in result :
		if file.endswith(x) :
			y.append(file)



#����� ����������� � �����������
ts = []
func_search(".ts",ts)



#����� ������ � ������ ffmpeg
for i in ts :
	command = 'ffmpeg -v error -i ' + i + ' -map 0:1 -f null - 2>' + i +'.log'
	os.system(command)



#����� ����� � ����������
log = []
func_search(".log",log)



#����� ������ � �����
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



#����� ����������� �� �����
print_Final_log = open('Final_log.txt','r')
print(print_Final_log.read())
