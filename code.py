#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 16:41:05 2022

@author: ertugruloney
"""
from gurobipy import GRB
import gurobipy as gp
import pandas as pd
import numpy as np


model=gp.Model("project")

#defing sets
Days=7
classes=31
boats=3
e1=1
e2=2
b=10

#defing parameters
f=[120,270,	82.5,	120,	225,	240,	15,	75	,75,	150,	150,
	75,	75,	90,	75,	150,	37.5,	30,	300,	150,	75,	90,
	150,	75,	150,	22.5,	97.5,	100,	45,	15,	135]
v=[3.2	,93,	0,	0,	88,	90.5,	68.95,	63.85,	63.85,	63.85,
	63.85,	0,	63.85,	63.85,	0,	0,	34.3,	21.9,	168.9,	168.9,
	63.85,	48.35,	63.85,	63.85,	63.85,	0	,0	,0,	63.85,	0,	131]
m=[2	,6,	6,	4,	6,	4,	6,	6,	6,	6,	6,	
      2	,2,	6,	6,	4,	10,	6,	2,	6,	6,	6,	
      4	,6,	6,	10,	4,	6,	6,	10,	6]
p=[350,	699,	399,	279,	599,	499,	179,	179,
	299,	399,	499,	299,	399,	395,	295,	399,	129,
	129,	899,	299	,299,	149,	495,	299,	495,	129,	595,	295,	129,	
    129	,399]
a=[2,	4,	4,	2,	5,	4,	0,	2,	2,	3,	4,	2,	2,	
   2,	2,	3,	0,	0,	6,	3,	2,	0,	4,	2,	4,	0,	
   2,	2,	1,	0,	2]
d=[[5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5
    ,5,5,5,5],
   [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5
       ,5,5,5,5],
   [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5
       ,5,5,5,5],
   [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5
       ,5,5,5,5],
   [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5
       ,5,5,5,5],
   [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5
       ,5,5,5,5],
   [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5
       ,5,5,5,5]]

l=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
u=[30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30]
#defing variables
x=model.addVars(classes,Days,name="x",lb=0,vtype="B")

y=model.addVars(classes,Days,name="y",lb=0,vtype="I")
#writing constraints
constraint1= model.addConstrs(y[i,t]<=m[i]*x[i,t] for i in range(classes) for t in range(Days))


constraint2_1= model.addConstrs((1-e1)*d[t][i]<=y[i,t]for t in range(Days)  for i in range(classes) )
constraint2_2= model.addConstrs((1+e2)*d[t][i]>=y[i,t]for t in range(Days)  for i in range(classes) )
constraint3=model.addConstrs(gp.quicksum(x[i,t] for i in range(classes))<=b for t in range(Days))

constraint4_1=model.addConstrs(gp.quicksum(x[i,t] for t in range(Days))>=l[i]for i in range(classes))

constraint4_2=model.addConstrs(gp.quicksum(x[i,t] for t in range(Days))<=u[i]for i in range(classes))

#objective function
model.setObjective(gp.quicksum(p[i]*y[i,t]-f[i]*x[i,t]-v[i]*y[i,t]for t in range(Days) for i in range(classes)),GRB.MAXIMIZE)
model.write("project.lp")
model.optimize()

#we see the values ​​of the variables
for v in model.getVars():
    print('%s %g' %(v.VarName,v.X))
    


