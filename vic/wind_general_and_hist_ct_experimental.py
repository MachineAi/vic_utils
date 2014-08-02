#cd Southwest Team Share

import os
import numpy as np
import pandas as pd
import netCDF4
from datetime import date
import pickle

'''
Prime Mover Types:
	BT = Binary cycle turbine
	CA = Combined cycle steam turbine
	CC = Combined cycle - total unit
	CE = Compressed air energy storage
c	CS = Combined cycle - single shaft
c	CT = Combined cycle combustion turbine
	FC = Fuel cell
c	GT = Combustion (gas) turbine
	HY = Hydraulic turbine
c	IC = Internal combustion (diesel)
c	IG = Integrated gasification combustion turbine
	OT = Other turbine
	PS = Hydraulic turbine - reversible (pumped storage)
s	PV = Photovoltaic
	ST = Steam turbine (boiler, nuclear, geothermal, and solar steam)
w	WT = Wind turbine 
'''

class get_cells():

		
	def __init__(self, tech):
			
		self.reg_conv = {'Arkansas-White-Red': 'arkred',
		'California' : 'cali',
		'Great Basin' : 'gbas',
		'Missouri' : 'mo',
		'Pacific Northwest' : 'pnw',
		'Rio Grande' : 'riog',
		'Upper Colorado' : 'colo',
		'Lower Colorado' : 'colo'}
		
		self.newold_conv = {'arkred': 'ark',
		'cali': 'cali',
		'gbas': 'grb',
		'mo' : 'mo',
		'pnw' : 'crb',
		'riog': 'rio',
		'colo' : 'color'}
		
		self.pp = {}
		self.diff_d = {}
		
		self.tech = pd.read_csv(tech).dropna(subset=['WRR'])
	
		for i in set(self.tech['WRR']):
			s_tech = self.tech.ix[self.tech['WRR'] == i]
			pp.update({self.reg_conv[i] : {}})
			for j, k in s_tech.iterrows():
				pp[self.reg_conv[i]].update({int(k['PCODE']) : (k['LAT'], k['LON'])})
		
		self.r_latlon = pickle.load( open( "./dict/region_latlon.p", "rb"))
		self.reg_latlon = {}
		self.reg_latlon['arkred'] = r_latlon['ark']
		self.reg_latlon['cali'] = r_latlon['cali']
		self.reg_latlon['colo'] = r_latlon['color']
		self.reg_latlon['gbas'] = r_latlon['grb']
		self.reg_latlon['mo'] = r_latlon['mo']
		self.reg_latlon['pnw'] = r_latlon['crb']
		self.reg_latlon['riog'] = r_latlon['rio']
	
		self.diff_d.update({tech : {}})
	
		
	def make_pp():
		temp_diff_d = {}
		for i in self.pp.keys():
			j_d = {}
	#		print os.getcwd()
			for j, k in self.pp[i].items():
				fn_d = {}
				j_d.update({j : None})
	#			print j_d
				lo = tuple([k[0], k[1]])
				for fn in reg_latlon[i]:
	#				fn_d = {}
					diff = ((fn[0] - lo[0])**2 + (fn[1] - lo[1])**2)**0.5
					fn_d.update({fn : diff})
				cell = min(fn_d, key=fn_d.get)
				mi = fn_d[cell]
				j_d[j] = cell		
			print j_d.items()
			temp_diff_d.update({i : j_d})
		self.diff_d[tech] = temp_diff_d
	
	
	def get_renhist():
		h = os.getcwd()
		print h
		for i in self.diff_d.keys():
			if not os.path.exists('%s' % (i)):
				os.mkdir('%s' % (i))
			for b in self.diff_d[i].keys():
				cv = self.newold_conv[b]
				if not os.path.exists('./%s/%s' % (i, cv)):
					os.mkdir('./%s/%s' % (i, cv))
				bdir = h + ('/%s/%s' % (i, cv))
				os.chdir('%s' % (self.newold_conv[b]))
				for j in diff_d[i][b].keys():
					print diff_d[i][b][j]
					shutil.copy('data_%s_%s' % (diff_d[i][b][j][0], diff_d[i][b][j][1]), bdir)
				os.chdir(h)
				
					
	
	
	def write_ren(old, hist):
		for i in diff_d.keys():
			if i == 'wind':
				print os.getcwd()
				os.chdir('./%s' % (i))
			for b in diff_d[i].keys():
				if old == False:
					os.chdir('./%s' % (b))
				elif old == True:
					os.chdir('./%s' % (self.newold_conv[b]))
				pp_d = {}
				for j in diff_d[i][b].keys():
					print diff_d[i][b][j]
					f = open('data_%s_%s' % (diff_d[i][b][j][0], diff_d[i][b][j][1]), 'r')
					r = f.readlines()
					f.close()
					print os.getcwd()
					w_li = []			
					for x in r:
						if hist == False:
							s = float(x.split()[3])
							w_li.append(s)
						elif hist == True:
							s = float(x.split()[6])
							w_li.append(s)
					w_s = pd.Series(w_li)
					pp_d.update({j : w_s})
	#			print pp_d
				pp_df = pd.DataFrame(pp_d)
				print pp_df
				pp_df.to_csv('%s_%s.csv' % (b, i))
				os.chdir('..')

#########Make latlon_d for solar to apply clips



pickle.dump(latlon_d, open('solar.p', 'wb'))

latlon_d = {}

for i in diff_d.keys():
	if i == 'solar':
		for b in diff_d[i].keys():
			ili = []
			ili.extend(diff_d[i][b].values())
			ili = list(set(ili))
			print ili
			latlon_d.update({self.newold_conv[b] : ili})
####################

make_wind()
make_solar()

####################

class makebasin():
	def __init__(self):

		self.region_df = {'arkred' : {}, 'cali' : {}, 'colo' : {}, 'gbas' : {}, 'mo' : {}, 'pnw' : {}, 'riog' : {}}
		self.region_dict = {'arkred' : [], 'cali' : [], 'colo' : [], 'gbas' : [], 'mo' : [], 'pnw' : [], 'riog' : []}
#		self.model = model
		
	def init_regdict(self):
		for fn in os.listdir('.'):
			if fn.endswith('nc'):
				for region in self.region_dict.keys():
					if region in fn[:6]:
						self.region_dict[region].append(fn)
	
		
	def make_reg_single(self, reg, type):
			
		nc = {}
		
		for fn in self.region_dict[reg]:
			if reg in diff_d[type].keys():
				f = netCDF4.Dataset(fn, 'r')								
				v = ''
				
				if fn[-12:-8] == 'prcp':
					v = 'prcp'
				
				if fn[-12:-8] == 'tmax':
					v = 'tmax'
					
				if fn[-12:-8] == 'tmin':
					v = 'tmin'
					
				if fn[-12:-8] == 'wind':
					v = 'wind'
				
				yr = fn[-7:-3]
				
				pan = pd.Panel(f.variables[v][:], items=f.variables['time'][:], major_axis=f.variables['lat'][:], minor_axis=f.variables['lon'][:])
				
				for i in diff_d[type][reg].values():
#					nc.update({i : {'prcp': {}, 'tmax': {}, 'tmin': {}, 'wind': {}}})
#					nc[i][v].update({yr:{}})
#					ilat = np.where(f.variables['lat'] == i[0])[0]
#					ilon = np.where(f.variables['lon'] == i[1])[0]
#					s = f.variables[v][:, ilat, ilon]
#					nc[i][v][yr] = s				
					if i[0] in pan.major_axis:
						if i[1] in pan.minor_axis:
							if i not in nc:
								nc.update({i : {'prcp': {}, 'tmax': {}, 'tmin': {}, 'wind': {}}})
							nc[i][v].update({yr:{}})
							s = pan.ix[:, i[0], i[1]]
							nc[i][v][yr] = s					
	
#			f.close()
			
		self.region_df[reg] = nc
		print self.region_df[reg]
				
	
	
	def write_files(self, reg, type):

		for i, v in self.region_df[reg].items():
			if not v == None:
				c_prcp = pd.concat(self.region_df[reg][i]['prcp'].values())
				c_tmax = pd.concat(self.region_df[reg][i]['tmax'].values())
				c_tmin = pd.concat(self.region_df[reg][i]['tmin'].values())
				c_wind = pd.concat(self.region_df[reg][i]['wind'].values())
			
				latlon_df = pd.concat([c_prcp, c_tmax, c_tmin, c_wind], axis=1)
				latlon_df.columns = ['prcp', 'tmax', 'tmin', 'wind']
#				latlon_df['date'] = [date.fromordinal(int(711858 + j)) for j in latlon_df.index]
#				latlon_df['mo'] = [j.month for j in latlon_df.date]
#				latlon_df['day'] = [j.day for j in latlon_df.date]
#				latlon_df['year'] = [j.year for j in latlon_df.date]
		
#				latlon_df['prcp_r'] = np.round(latlon_df['prcp'], 2)
#				latlon_df['tmax'] = np.round(latlon_df['tmax'], 2)
#				latlon_df['tmin'] = np.round(latlon_df['tmin'], 2)
#				latlon_df['wind'] = np.round(latlon_df['wind'], 2)
				
				latlon_df = latlon_df[['prcp', 'tmax', 'tmin', 'wind']]				
				
				if not os.path.exists('%s' % (type)):
					os.mkdir('%s' % (type))
				if not os.path.exists('./%s/%s' % (type, reg)):
					os.mkdir('./%s/%s' % (type, reg))
				else:
					pass
				latlon_df.to_csv('./%s/%s/data_%s_%s' % (type, reg, i[0], i[1]), sep=" ", header=False, index=False)
			
	def basin_all(self, type):
		
		self.init_regdict()
		for i in self.region_df.keys():
			self.region_df = {'arkred' : {}, 'cali' : {}, 'colo' : {}, 'gbas' : {}, 'mo' : {}, 'pnw' : {}, 'riog' : {}}
			print i
			self.make_reg_single(i, type)
			self.write_files(i, type)


###########################
mb = makebasin()
mb.basin_all('wind')
mb.basin_all('solar')
###########################

import shutil

#cd 'C:\Users\Matt Bartos\Desktop\a1b'


#		os.chdir('..')
		
write_ren()

