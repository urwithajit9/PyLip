import cv2
import numpy as np
from roifinder import ROIFind
class LipShape:
	def __init__(self,image):	
		np.seterr(divide='ignore')
		roiFind = ROIFind(image)
		img = roiFind.getROIImage()
		im = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

		b,g,r = cv2.split(img)
		h,s,v = cv2.split(img)
		phue = np.divide(r,g+r) 

		norm_phue = phue / 255.0
		norm_lum = v / 255.0
		r_supx,r_supy = np.gradient(norm_phue - norm_lum)
		#print r_supx,r_supy

		r_inf = np.diff(norm_phue + norm_lum , n=1,axis=1)
		#print r_inf
	def drawLipRegion():
		return None

	def d(x,y0,y1):
		return (norm_phue[y0:y1,x] - norm_lum[y0:y1,x]).sum()

	def findUpperPoints():
		r_supMin, m, n  = 100, 0, 0
		for i in range(4,10):
			for j in range(img.shape[1]):
				if r_supy[i][j] < r_supMin:
					m = i
					n = j
					r_supMin = r_supy[i][j]
	
		print 'Initial position is ',m,n
		cupidon =[]
		while m > 3:
			r_per = [0.0,0.0,0.0]
			r_per[0] = np.dot((0, 1), (r_supx[m,n+1],r_supy[m,n+1]))
			r_per[1] = np.dot((1,-1), (r_supx[m-1,n+1],r_supy[m-1,n+1]))
			r_per[2] = np.dot((-1, -1), (r_supx[m+1,n+1],r_supy[m+1,n+1]))
			
			print r_per	
			per_max, k = -99, -1
			for i in range(3):
				if per_max < r_per[i]:
					per_max = r_per[i]
					k = i
		
			if k == 0:
				n = n +1
			elif k == 1:
				m = m - 1
				n = n +1
			elif k == 2:
				m = m + 1
				n = n + 1
			else:
				print 'Something buggy happening here'
			print m,n	
			cv2.rectangle(img,(n,m),(n+3,m+3),(0,0,0),1)
			cv2.imshow('testing',img)
			cupidon.append((m,n))
	
		print 'cupidon values are',cupidon
		darray = []
		for x,y in cupidon:
			darray.append((d(x,4,10),x,y))
		darray.sort()
		p3 = darray[0]
		if darray[-1][1] < darray[-2][1] :
			p2 = darray[-1]
			p4 = darray[-2] 
		else:
			p2 = darray[-2]
			p4 = darray[-1] 
	
	
		return p2[1:],p3[1:],p4[1:]
	
	def findLipCorners():
		lum_min ,ymini= 999999999999,0
		for i in range(v.shape[0]):
			lum_sum = v[i].sum()
			if lum_sum < lum_min:
				lum_min = lum_sum
				ymini = i
		ymini_mean = lum_min
		p1, p5 = (0,0),(0,0)
		for i in range(v.shape[1]):
			if v[ymini][i] <ymini_mean:
				p1 = (ymini,i)
		for i in range( v.shape[1]-1,0,-1):
			if v[ymini][i]<ymini_mean:
				p5 = (ymini,i)
		return p1,p5
	
	def findLowerPoint():
		p1,p5 = findLipCorners()
		y = (p1[1] + p5[1])/2
		min, p6= 9999999, (0,0)
		for i in range(p1[0],v.shape[0]):
			if min > r_inf[i][y]:
				min = r_inf[i][y]
				p6 = (i,y)
		return p6
	
	def cubic_function(a,b,c,d,x0,x1):
		ip = range(x0,x1,1)
		op = np.zeros((x1-x0,2))
		for i in range(len(ip)):
			x = ip[i]
			op[i,1],op[i,0] = x, a*x**3 + b*x**2 + c *x + d
		return op
	
	def theta_sup(vector):
		theta = 0
		ds = np.diff(vector)
		dn = [-1 *ds[1],ds[0]]
		print "ds shape = ",ds.shape
		print "r_supx shape",r_supx.shape
		a = 0
		for i in vector:
			x,y = int(i[0]),int(i[1])
			a = a + np.dot((r_supx[x,y],r_supy[x,y]),dn)
		b = np.trapz(ds) 
		theta = a / b
		return theta
	
	def theta_inf(vector):
		theta = 0
		ds = np.diff(vector)
		dn = [-1 * ds[1], ds[0]]
		r_huex, r_huey = np.gradient(norm_phue)
		a = 0
		for i in vector:
			x,y = int(i[0]),int(i[1])
			a = a + np.dot((r_huex[x,y],r_huey[x,y]),dn)
		b = np.trapz(ds) 
		theta = a / b
		return theta
	
	def detectLipEdge(point1,point2,theta_fun):
		x0,y0 = point1
		x1,y1 = point2
		min,k = 9999,(0,0,0,0)
		for b in range(0,5,1):
			a = (y1 - y0 + ((x1*x1) - (x0*x0))) / (x1*x1*x1 - x0*x0*x0)
			c = ((-3.0)*a*x1 *x1) + ((-2) * b * x1)
			d = y1 - (a * x1 * x1 * x1) - (b * x1 * x1) - (c * x1)
			fun_vector = cubic_function(a,b,c,d,y0,y1)
			theta  = theta_fun(fun_vector)
			if theta < min :
				min = theta
				k = (a,b,c,d)
		return k
