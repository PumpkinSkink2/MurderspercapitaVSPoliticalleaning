import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score
import csv

def slice_List(sourcelist,stepsize):
	"""slices a list(sourcelist) into a stepsize. careful that your stepsize actually divides into the length of the list."""
	sliced_list = []
	listlen = int(round(len(sourcelist)/stepsize))

	for i in range(listlen):
		sliced_list.append(sourcelist[(i*stepsize):((i*stepsize)+stepsize):])
	return(sliced_list)
	return temp_list
def sort_key(sourcelist):
	return(float(sourcelist[2]))

with open('Murderpercapita.csv', 'r', encoding = 'utf=8', newline = '') as data_file:
	reader = csv.reader(data_file) 
	murderpercapita_data = list(reader)
	# murderpercapita_data = data_file.read()

with open('States.csv', 'r', encoding = 'utf=8', newline = '') as data_file:
	reader = csv.reader(data_file) 
	lean_data = list(reader)
for i in murderpercapita_data:
	del(i[4])

for i in lean_data:
	for j in murderpercapita_data:
		if i[1] == j[1]:
			j.append(i[2])
murderpercapita_data[0].append('LEAN')

temp_list = []
for i in murderpercapita_data:
	if i[0] == '2020':
		temp_list.append(i)
murderpercapita_data = temp_list
murderpercapita_data.sort(key = sort_key)

for i in murderpercapita_data:
	if i[1] == 'NH':
		print(i)
state = []
murderpercapita = []
lean = []

for i in murderpercapita_data:
	state.append(i[1])
	murderpercapita.append(float(i[2]))
	lean.append(float(i[4]))


width = 1

def colorgrad(v):
	colormap = ['#FE433C', '#F31D64', '#A224AD', '#6A38B3','#3C50B1','#0095EF']
	norm = ((max(lean))-(min(lean)))
	level1 = min(lean)+((1/6)*norm)
	level2 = min(lean)+((2/6)*norm)
	level3 = min(lean)+((3/6)*norm)
	level4 = min(lean)+((4/6)*norm)
	level5 = min(lean)+((5/6)*norm)
	level6 = min(lean)+((6/6)*norm)

	if v < level1:
		return(colormap[0])
	if v < level2:
		return(colormap[1])
	if v < level3:
		return(colormap[2])
	if v < level4:
		return(colormap[3])
	if v < level5:
		return(colormap[4])
	if v <= level6:
		return(colormap[5])
	else:
		return('#000000')

colors = []
for i in lean:
	j = colorgrad(i)
	colors.append(j)
colors = np.array(colors)

x = lean
y = murderpercapita
reg_params = np.polyfit(x,y,1)
trend = np.poly1d(reg_params)
R = ()
text = ('Slope = ' + str("{:.2e}".format(reg_params[0], 4)) + '\n' + 'Int = '+ str(round(reg_params[1], 2)) + '\n' + 'R2 = ' + str(round(r2_score(y, trend(x)),3)))

plt.style.use('seaborn-dark-palette')

fig, ax = plt.subplots(2,1)

ax[0].bar(state,murderpercapita, width, color = colors, label = 'Murder rate per 1000 people')
ax[0].set(xlabel = 'State', ylabel = 'Murders per 1000 people')

ax[1].scatter(x,y, c = colors)
ax[1].plot(x,trend(x), color = 'black', alpha = 0.5)
ax[1].set( xlabel = 'Political Slant', ylabel = 'Murders per 1000 people')
ax[1].text(0.05, 0.95, text,transform=plt.gca().transAxes,
     fontsize=10, verticalalignment='top')
for w,z in zip(x,y):
	k = x.index(w) 
	label = state[k]
	ax[1].annotate(label, (w,z), textcoords = "offset points", xytext = (0,5), ha = 'center')

plt.show()