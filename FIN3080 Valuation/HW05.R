library(openxlsx)
library(readxl)
library(dplyr)
library(ggplot2)
library(tidyverse)
library(zoo)
library(imputeTS)

##Step2
#回报率导入
data1 = read_xlsx('D:/z桌面/新建文件夹/FIN3080/HW5/Daily Stock Price  Returns141452348/TRD_Dalyr.xlsx')
data1 = data1[-1:-2,]
data2 = read_xlsx('D:/z桌面/新建文件夹/FIN3080/HW5/Daily Stock Price  Returns141452348/TRD_Dalyr1.xlsx')
data2 = data2[-1:-2,]
data3 = read_xlsx('D:/z桌面/新建文件夹/FIN3080/HW5/Daily Stock Price  Returns141452348/TRD_Dalyr2.xlsx')
data3 = data3[-1:-2,]
data4 = read_xlsx('D:/z桌面/新建文件夹/FIN3080/HW5/Daily Stock Price  Returns141452348/TRD_Dalyr3.xlsx')
data4 = data4[-1:-2,]
data5 = read_xlsx('D:/z桌面/新建文件夹/FIN3080/HW5/Daily Stock Price  Returns141452348/TRD_Dalyr4.xlsx')
data5 = data5[-1:-2,]
data6 = read_xlsx('D:/z桌面/新建文件夹/FIN3080/HW5/Daily Stock Price  Returns141452348/TRD_Dalyr5.xlsx')
data6 = data6[-1:-2,]
data7 = read_xlsx('D:/z桌面/新建文件夹/FIN3080/HW5/Daily Stock Price  Returns140408718/TRD_Dalyr.xlsx')
data7 = data7[-1:-2,]
data8 = read_xlsx('D:/z桌面/新建文件夹/FIN3080/HW5/Daily Stock Price  Returns140408718/TRD_Dalyr1.xlsx')
data8 = data8[-1:-2,]
data9 = read_xlsx('D:/z桌面/新建文件夹/FIN3080/HW5/Daily Stock Price  Returns140408718/TRD_Dalyr2.xlsx')
data9 = data9[-1:-2,]
data10 = read_xlsx('D:/z桌面/新建文件夹/FIN3080/HW5/Daily Stock Price  Returns140408718/TRD_Dalyr3.xlsx')
data10 = data10[-1:-2,]

#数据整合
data = rbind(data1,data2,data3,data4,data5,data6,data7,data8,data9,data10)
colnames(data) = c('id','date','ret')
data$ret = as.numeric(data$ret)

#排除非主板
data$str=substr(data$id,start = 1, stop=2)
data=data[data$str%in%c('00','60'),]
data=data%>%group_by(id)%>%arrange(date)
data=data%>%arrange(id)

#导入mkt数据
rm = read_xlsx('D:/z桌面/新建文件夹/FIN3080/HW5/Aggregated Daily Market Returns183830444/mkt.xlsx')
rm = rm[-1:-2,]
rm = rm %>% filter(Markettype=='5.0')
rm = rm[,-1]
colnames(rm) = c('date','rm')
rm$rm = as.numeric(rm$rm)

#表格合并
data = data %>% left_join(rm,by = 'date')
#处理rm中缺失值
data = data %>% 
  mutate(rm = na_ma(rm)) %>% ungroup()
data = data %>% mutate(ret.rm=ret-rm)



###步骤1 eps 的处理
rep = read.xlsx('D:/z桌面/新建文件夹/FIN3080/HW5/Index per Share095511626/FI_T9.xlsx')
rep = rep[-1:-2,]
#排除母表
rep=rep[rep$Typrep=='A',]
rep=rep[,-4]
colnames(rep) = c('id','type','date','eps')
#step 1.8
andate=read.xlsx('D:/z桌面/新建文件夹/FIN3080/HW5/Statements Release Dates174006211/IAR_Rept.xlsx')
andate=andate[-1:-2,]
colnames(andate)=c('id','type','timetype','date','andate')
rep=left_join(rep,andate,by=c('id','date','type'))


rep$eps = as.numeric(rep$eps)
#step 1.3
rep$str=substr(rep$date,start = 6, stop=7)
rep=rep[rep$str%in%c('06','12'),]
rep$str1=substr(rep$date,start = 1, stop=4)
rep = rep %>% group_by(id,str1) %>%
  mutate(eps1 = lag(eps,1)) %>%
  ungroup()
rep$eps1[is.na(rep$eps1)]=0
rep$eps=rep$eps-rep$eps1
rep=rep[,c(1,2,5,4,6,3)]

#step1.4     ###Event从2015H2开始
rep = rep %>% group_by(id) %>%
  mutate(ue = eps-lag(eps,2)) %>%
  ungroup() %>%
  na.omit()
#step 1.5
rep = rep %>% group_by(id) %>%
  mutate(mu = (ue+lag(ue)+lag(ue,2)+lag(ue,3))/4) %>%
  mutate(sigma = ((ue-mu)^2+(lag(ue)-mu)^2+(lag(ue,2)-mu)^2+(lag(ue,3)-mu)^2)^0.5/2) %>%
  mutate(sue = ue/sigma) %>% ungroup()
rep = rep %>% select(id,andate,eps,sue,type,timetype,date) %>% na.omit()
rep$yy=substr(rep$date,start = 1,stop = 4)

#step1.6
p = c(0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9)
bp = rep %>% group_by(yy,timetype) %>%
  summarise(part.port = list(paste0(p*100,"%")),
            break.point = list(quantile(sue, p, type=3)))%>% 
  unnest(cols=c(qt,break.point)) %>% ungroup()
bp = spread(bp,"qt","break.point")
port = rep %>% group_by(yy,timetype) %>%
  mutate(group= 
           cut(sue,breaks=c(min(sue),
                            quantile(sue,p,type=3),
                            max(sue)),
               include.lowest = T,
               order_result = T,
               labels=seq(1,10))) %>% ungroup()
port$str=substr(port$type,start = 1,stop = 2)
port$str1=substr(port$type,start = 2,stop = 3)
port=port[!(port$str%in%c('ST','PT')),]#删除ST PT
port=port[!(port$str1%in%c('ST','PT')),] #删除ST PT


##step3.1
#数据预处理（数据合并与标号）
new_data <- data %>%
  rename(andate = date)
new_data=new_data[,-4]
port=port[,-c(5,10,11)]
data = new_data %>% full_join(port,by=c('andate','id'))

data <- data %>%
  rename(andate=date,date=andate)

data = data %>% 
  mutate(flag = ifelse(type=='4.0'&yy=='2015',1,flag)) %>%
  mutate(flag = ifelse(type=='2.0'&yy=='2016',2,flag)) %>%
  mutate(flag = ifelse(type=='4.0'&yy=='2016',3,flag)) %>%
  mutate(flag = ifelse(type=='2.0'&yy=='2017',4,flag)) %>%
  mutate(flag = ifelse(type=='4.0'&yy=='2017',5,flag)) %>%
  mutate(flag = ifelse(type=='2.0'&yy=='2018',6,flag)) %>%
  mutate(flag = ifelse(type=='4.0'&yy=='2018',7,flag)) %>%
  mutate(flag = ifelse(type=='2.0'&yy=='2019',8,flag)) %>%
  mutate(flag = ifelse(type=='4.0'&yy=='2019',9,flag))%>%
  mutate(flag = ifelse(type=='2.0'&yy=='2020',10,flag))%>%
  mutate(flag = ifelse(type=='4.0'&yy=='2020',11,flag))%>%
  mutate(flag = ifelse(type=='2.0'&yy=='2021',12,flag))%>%
  mutate(flag = ifelse(type=='4.0'&yy=='2021',13,flag))%>%
  mutate(flag = ifelse(type=='2.0'&yy=='2022',14,flag))

data = data %>% mutate(index = c(1:nrow(data)))
data = data %>%
  mutate(flag = ifelse(is.na(flag),0,flag))

#3.2循环
n<- which(data$date=="2015-12-31" & data$andate != 0)
for (i in 1:1449){
  data$t1[n[i]-120]=data$ret.rm[n[i]-120]
  for (j in -119:120){
    data$t1[n[i]+j]=data$t1[n[i]+j-1]+data$ret.rm[n[i]+j]
  }
}
n<- which(data$date=="2016-06-30" & data$andate != 0)

for (i in 1:1470){
  data$t2[n[i]-120]=data$ret.rm[n[i]-120]
  for (j in -119:120){
    data$t2[n[i]+j]=data$t2[n[i]+j-1]+data$ret.rm[n[i]+j]
  }
}
n<- which(data$date=="2016-12-31" & data$andate != 0)
for (i in 1:1464){
  data$t3[n[i]-120]=data$ret.rm[n[i]-120]
  for (j in -119:120){
    data$t3[n[i]+j]=data$t3[n[i]+j-1]+data$ret.rm[n[i]+j]
  }
}
n<- which(data$date=="2017-06-30" & data$andate != 0)
for (i in 1:1662){
  data$t4[n[i]-120]=data$ret.rm[n[i]-120]
  for (j in -119:120){
    data$t4[n[i]+j]=data$t4[n[i]+j-1]+data$ret.rm[n[i]+j]
  }
}
n<- which(data$date=="2017-12-31" & data$andate != 0)
for (i in 1:1651){
  data$t5[n[i]-120]=data$ret.rm[n[i]-120]
  for (j in -119:120){
    data$t5[n[i]+j]=data$t5[n[i]+j-1]+data$ret.rm[n[i]+j]
  }
}
n<- which(data$date=="2018-06-30" & data$andate != 0)
for (i in 1:1927){
  data$t6[n[i]-120]=data$ret.rm[n[i]-120]
  for (j in -119:120){
    data$t6[n[i]+j]=data$t6[n[i]+j-1]+data$ret.rm[n[i]+j]
  }
}
n<- which(data$date=="2018-12-31" & data$andate != 0)
for (i in 1:1917){
  data$t7[n[i]-120]=data$ret.rm[n[i]-120]
  for (j in -119:120){
    data$t7[n[i]+j]=data$t7[n[i]+j-1]+data$ret.rm[n[i]+j]
  }
}
n<- which(data$date=="2019-06-30" & data$andate != 0)
for (i in 1:2046){
  data$t8[n[i]-120]=data$ret.rm[n[i]-120]
  for (j in -119:120){
    data$t8[n[i]+j]=data$t8[n[i]+j-1]+data$ret.rm[n[i]+j]
  }
}
n<- which(data$date=="2019-12-31" & data$andate != 0)
for (i in 1:2155){
  data$t9[n[i]-120]=data$ret.rm[n[i]-120]
  for (j in -119:120){
    data$t9[n[i]+j]=data$t9[n[i]+j-1]+data$ret.rm[n[i]+j]
  }
}
n<- which(data$date=="2020-06-30" & data$andate != 0)
for (i in 1:1966){
  data$t10[n[i]-120]=data$ret.rm[n[i]-120]
  for (j in -119:120){
    data$t10[n[i]+j]=data$t10[n[i]+j-1]+data$ret.rm[n[i]+j]
  }
}
n<- which(data$date=="2020-12-31" & data$andate != 0)
for (i in 1:2333){
  data$t11[n[i]-120]=data$ret.rm[n[i]-120]
  for (j in -119:120){
    data$t11[n[i]+j]=data$t11[n[i]+j-1]+data$ret.rm[n[i]+j]
  }
}
n<- which(data$date=="2021-06-30" & data$andate != 0)
for (i in 1:2102){
  data$t12[n[i]-120]=data$ret.rm[n[i]-120]
  for (j in -119:120){
    data$t12[n[i]+j]=data$t12[n[i]+j-1]+data$ret.rm[n[i]+j]
  }
}
n<- which(data$date=="2021-12-31" & data$andate != 0)
for (i in 1:2173){
  data$t13[n[i]-120]=data$ret.rm[n[i]-120]
  for (j in -119:120){
    data$t13[n[i]+j]=data$t13[n[i]+j-1]+data$ret.rm[n[i]+j]
  }
}
n<- which(data$date=="2022-06-30" & data$andate != 0)
for (i in 1:2341){
  data$t14[n[i]-120]=data$ret.rm[n[i]-120]
  for (j in -119:120){
    data$t14[n[i]+j]=data$t14[n[i]+j-1]+data$ret.rm[n[i]+j]
  }
}

data=data%>%
  select(part.port,t1)%>%
  mutate(index=0)
data=data%>%
  filter(t1!=0)
n<- which(is.na(data$part.port)==F)

for (i in seq(from=121,to=max(n),by=241)){
  data$index[i-120]=-120
  data$part.port[i-120]=data$part.port[i]
  for (j in -119:120){
    data$index[i+j]=data$index[i+j-1]+1
    data$part.port[i+j]=data$part.port[i]
  }
}
colnames(data)=c('part.port','CAR','index')

##cumsum
data = data %>% group_by(id) %>%
  mutate(t.1=cumsum(t1)) %>%
  mutate(t.1 = ifelse(t.1==lag(t.1),0,t.1)) %>%
  mutate(t.1 = ifelse(is.na(t.1),t1,t.1)) %>% 
  mutate(t.1 = ifelse(t.1>241,0,t.1)) %>%
  mutate(t.1 = ifelse(t.1-lag(t.1)!=1,0,t.1)) %>%
  mutate(t.1 = ifelse(is.na(t.1),t1,t.1)) %>%
  ungroup()
data = data %>% group_by(id) %>%
  mutate(t.1 = ifelse(t.1!=0,t.1-ceiling(max(t.1)/2)+0.01,t.1)) %>% ungroup()

data = data %>% group_by(id) %>%
  mutate(t.2=cumsum(t2)) %>%
  mutate(t.2 = ifelse(t.2==lag(t.2),0,t.2)) %>%
  mutate(t.2 = ifelse(is.na(t.2),t2,t.2)) %>% 
  mutate(t.2 = ifelse(t.2>241,0,t.2)) %>%
  mutate(t.2 = ifelse(t.2-lag(t.2)!=1,0,t.2)) %>%
  mutate(t.2 = ifelse(is.na(t.2),t2,t.2)) %>%
  ungroup()
data = data %>% group_by(id) %>%
  mutate(t.2 = ifelse(t.2!=0,t.2-ceiling(max(t.2)/2)+0.01,t.2)) %>% ungroup()

data = data %>% group_by(id) %>%
  mutate(t.3=cumsum(t3)) %>%
  mutate(t.3 = ifelse(t.3==lag(t.3),0,t.3)) %>%
  mutate(t.3 = ifelse(is.na(t.3),t3,t.3)) %>% 
  mutate(t.3 = ifelse(t.3>241,0,t.3)) %>%
  mutate(t.3 = ifelse(t.3-lag(t.3)!=1,0,t.3)) %>%
  mutate(t.3 = ifelse(is.na(t.3),t3,t.3)) %>%
  ungroup()
data = data %>% group_by(id) %>%
  mutate(t.3 = ifelse(t.3!=0,t.3-ceiling(max(t.3)/2)+0.01,t.3)) %>% ungroup()

data = data %>% group_by(id) %>%
  mutate(t.4=cumsum(t4)) %>%
  mutate(t.4 = ifelse(t.4==lag(t.4),0,t.4)) %>%
  mutate(t.4 = ifelse(is.na(t.4),t4,t.4)) %>% 
  mutate(t.4 = ifelse(t.4>241,0,t.4)) %>%
  mutate(t.4 = ifelse(t.4-lag(t.4)!=1,0,t.4)) %>%
  mutate(t.4 = ifelse(is.na(t.4),t4,t.4)) %>%
  ungroup()
data = data %>% group_by(id) %>%
  mutate(t.4 = ifelse(t.4!=0,t.4-ceiling(max(t.4)/2)+0.01,t.4)) %>% ungroup()

data = data %>% group_by(id) %>%
  mutate(t.5=cumsum(t5)) %>%
  mutate(t.5 = ifelse(t.5==lag(t.5),0,t.5)) %>%
  mutate(t.5 = ifelse(is.na(t.5),t5,t.5)) %>% 
  mutate(t.5 = ifelse(t.5>241,0,t.5)) %>%
  mutate(t.5 = ifelse(t.5-lag(t.5)!=1,0,t.5)) %>%
  mutate(t.5 = ifelse(is.na(t.5),t5,t.5)) %>%
  ungroup()
data = data %>% group_by(id) %>%
  mutate(t.5 = ifelse(t.5!=0,t.5-ceiling(max(t.5)/2)+0.01,t.5)) %>% ungroup()

data = data %>% group_by(id) %>%
  mutate(t.6=cumsum(t6)) %>%
  mutate(t.6 = ifelse(t.6==lag(t.6),0,t.6)) %>%
  mutate(t.6 = ifelse(is.na(t.6),t6,t.6)) %>% 
  mutate(t.6 = ifelse(t.6>241,0,t.6)) %>%
  mutate(t.6 = ifelse(t.6-lag(t.6)!=1,0,t.6)) %>%
  mutate(t.6 = ifelse(is.na(t.6),t6,t.6)) %>%
  ungroup()
data = data %>% group_by(id) %>%
  mutate(t.6 = ifelse(t.6!=0,t.6-ceiling(max(t.6)/2)+0.01,t.6)) %>% ungroup()

data = data %>% group_by(id) %>%
  mutate(t.7=cumsum(t7)) %>%
  mutate(t.7 = ifelse(t.7==lag(t.7),0,t.7)) %>%
  mutate(t.7 = ifelse(is.na(t.7),t7,t.7)) %>% 
  mutate(t.7 = ifelse(t.7>241,0,t.7)) %>%
  mutate(t.7 = ifelse(t.7-lag(t.7)!=1,0,t.7)) %>%
  mutate(t.7 = ifelse(is.na(t.7),t7,t.7)) %>%
  ungroup()
data = data %>% group_by(id) %>%
  mutate(t.7 = ifelse(t.7!=0,t.7-ceiling(max(t.7)/2)+0.01,t.7)) %>% ungroup()

data = data %>% group_by(id) %>%
  mutate(t.8=cumsum(t8)) %>%
  mutate(t.8 = ifelse(t.8==lag(t.8),0,t.8)) %>%
  mutate(t.8 = ifelse(is.na(t.8),t8,t.8)) %>% 
  mutate(t.8 = ifelse(t.8>241,0,t.8)) %>%
  mutate(t.8 = ifelse(t.8-lag(t.8)!=1,0,t.8)) %>%
  mutate(t.8 = ifelse(is.na(t.8),t8,t.8)) %>%
  ungroup()
data = data %>% group_by(id) %>%
  mutate(t.8 = ifelse(t.8!=0,t.8-ceiling(max(t.8)/2)+0.01,t.8)) %>% ungroup()

data = data %>% group_by(id) %>%
  mutate(t.9=cumsum(t9)) %>%
  mutate(t.9 = ifelse(t.9==lag(t.9),0,t.9)) %>%
  mutate(t.9 = ifelse(is.na(t.9),t9,t.9)) %>% 
  mutate(t.9 = ifelse(t.9>241,0,t.9)) %>%
  mutate(t.9 = ifelse(t.9-lag(t.9)!=1,0,t.9)) %>%
  mutate(t.9 = ifelse(is.na(t.9),t9,t.9)) %>%
  ungroup()
data = data %>% group_by(id) %>%
  mutate(t.9 = ifelse(t.9!=0,t.9-ceiling(max(t.9)/2)+0.01,t.9)) %>% ungroup()

data = data %>% group_by(id) %>%
  mutate(t.10=cumsum(t10)) %>%
  mutate(t.10 = ifelse(t.10==lag(t.10),0,t.10)) %>%
  mutate(t.10 = ifelse(is.na(t.10),t10,t.10)) %>% 
  mutate(t.10 = ifelse(t.10>241,0,t.10)) %>%
  mutate(t.10 = ifelse(t.10-lag(t.10)!=1,0,t.10)) %>%
  mutate(t.10 = ifelse(is.na(t.10),t10,t.10)) %>%
  ungroup()
data = data %>% group_by(id) %>%
  mutate(t.10 = ifelse(t.10!=0,t.10-ceiling(max(t.10)/2)+0.01,t.10)) %>% ungroup()

data = data %>% group_by(id) %>%
  mutate(t.11=cumsum(t11)) %>%
  mutate(t.11 = ifelse(t.11==lag(t.11),0,t.11)) %>%
  mutate(t.11 = ifelse(is.na(t.11),t11,t.11)) %>% 
  mutate(t.11 = ifelse(t.11>241,0,t.11)) %>%
  mutate(t.11 = ifelse(t.11-lag(t.11)!=1,0,t.11)) %>%
  mutate(t.11 = ifelse(is.na(t.11),t11,t.11)) %>%
  ungroup()

data = data %>% group_by(id) %>%
  mutate(t.12=cumsum(t12)) %>%
  mutate(t.12 = ifelse(t.12==lag(t.12),0,t.12)) %>%
  mutate(t.12 = ifelse(is.na(t.12),t12,t.12)) %>% 
  mutate(t.12 = ifelse(t.12>241,0,t.12)) %>%
  mutate(t.12 = ifelse(t.12-lag(t.12)!=1,0,t.12)) %>%
  mutate(t.12 = ifelse(is.na(t.12),t12,t.12)) %>%
  ungroup()

data = data %>% group_by(id) %>%
  mutate(t.13=cumsum(t13)) %>%
  mutate(t.13 = ifelse(t.13==lag(t.13),0,t.13)) %>%
  mutate(t.13 = ifelse(is.na(t.13),t13,t.13)) %>% 
  mutate(t.13 = ifelse(t.13>241,0,t.13)) %>%
  mutate(t.13 = ifelse(t.13-lag(t.13)!=1,0,t.13)) %>%
  mutate(t.13 = ifelse(is.na(t.13),t13,t.13)) %>%
  ungroup()

data = data %>% group_by(id) %>%
  mutate(t.14=cumsum(t14)) %>%
  mutate(t.14 = ifelse(t.14==lag(t.14),0,t.14)) %>%
  mutate(t.14 = ifelse(is.na(t.14),t14,t.14)) %>% 
  mutate(t.14 = ifelse(t.14>241,0,t.14)) %>%
  mutate(t.14 = ifelse(t.14-lag(t.14)!=1,0,t.14)) %>%
  mutate(t.14 = ifelse(is.na(t.14),t14,t.14)) %>%
  ungroup()

data = data %>% group_by(id) %>%
  mutate(t.14 = ifelse(t.14!=0,t.14-ceiling(max(t.14)/2)+0.01,t.14)) %>% ungroup()

d1 = data %>% filter(t.1 != 0) %>%
  select(id,date,ret.rm,t.1) %>% group_by(id) %>%
  mutate(cum = cumsum(ret.rm))
p1 = port %>% filter(type=='2.0'&yy=='2015') %>%
  select(id,type,yy,group)
d1 = d1 %>% left_join(p1,by='id')
d.1 = d1 %>% group_by(group,t.1) %>%
  summarise(cum = mean(cum,na.rm=T)) %>%
  ungroup()
d.1 = d.1 %>% na.omit() %>%
  mutate(t.1 = t.1-0.01)
colnames(d.1) = c('group','t','cum')

d2 = data %>% filter(t.2 != 0) %>%
  select(id,date,ret.rm,t.2) %>% group_by(id) %>%
  mutate(cum = cumsum(ret.rm))
p2 = port %>% filter(type=='4.0'&yy=='2015') %>%
  select(id,type,yy,group)
d2 = d2 %>% left_join(p2,by='id')
d.2 = d2 %>% group_by(group,t.2) %>%
  summarise(cum = mean(cum,na.rm=T)) %>%
  ungroup()
d.2 = d.2 %>% na.omit() %>%
  mutate(t.2 = t.2-0.01)
colnames(d.2) = c('group','t','cum')

d3 = data %>% filter(t.3 != 0) %>%
  select(id,date,ret.rm,t.3) %>% group_by(id) %>%
  mutate(cum = cumsum(ret.rm))
p3 = port %>% filter(type=='2.0'&yy=='2016') %>%
  select(id,type,yy,group)
d3 = d3 %>% left_join(p3,by='id')
d.3 = d3 %>% group_by(group,t.3) %>%
  summarise(cum = mean(cum,na.rm=T)) %>%
  ungroup()
d.3 = d.3 %>% na.omit() %>%
  mutate(t.3 = t.3-0.01)
colnames(d.3) = c('group','t','cum')

d4 = data %>% filter(t.4 != 0) %>%
  select(id,date,ret.rm,t.4) %>% group_by(id) %>%
  mutate(cum = cumsum(ret.rm))
p4 = port %>% filter(type=='4.0'&yy=='2016') %>%
  select(id,type,yy,group)
d4 = d4 %>% left_join(p4,by='id')
d.4 = d4 %>% group_by(group,t.4) %>%
  summarise(cum = mean(cum,na.rm=T)) %>%
  ungroup()
d.4 = d.4 %>% na.omit() %>%
  mutate(t.4 = t.4-0.01)
colnames(d.4) = c('group','t','cum')

d5 = data %>% filter(t.5 != 0) %>%
  select(id,date,ret.rm,t.5) %>% group_by(id) %>%
  mutate(cum = cumsum(ret.rm))
p5 = port %>% filter(type=='2.0'&yy=='2017') %>%
  select(id,type,yy,group)
d5 = d5 %>% left_join(p5,by='id')
d.5 = d5 %>% group_by(group,t.5) %>%
  summarise(cum = mean(cum,na.rm=T)) %>%
  ungroup()
d.5 = d.5 %>% na.omit() %>%
  mutate(t.5 = t.5-0.01)
colnames(d.5) = c('group','t','cum')

d6 = data %>% filter(t.6 != 0) %>%
  select(id,date,ret.rm,t.6) %>% group_by(id) %>%
  mutate(cum = cumsum(ret.rm))
p6 = port %>% filter(type=='4.0'&yy=='2017') %>%
  select(id,type,yy,group)
d6 = d6 %>% left_join(p6,by='id')
d.6 = d6 %>% group_by(group,t.6) %>%
  summarise(cum = mean(cum,na.rm=T)) %>%
  ungroup()
d.6 = d.6 %>% na.omit() %>%
  mutate(t.6 = t.6-0.01)
colnames(d.6) = c('group','t','cum')

d7 = data %>% filter(t.7 != 0) %>%
  select(id,date,ret.rm,t.7) %>% group_by(id) %>%
  mutate(cum = cumsum(ret.rm))
p7 = port %>% filter(type=='2.0'&yy=='2018') %>%
  select(id,type,yy,group)
d7 = d7 %>% left_join(p7,by='id')
d.7 = d7 %>% group_by(group,t.7) %>%
  summarise(cum = mean(cum,na.rm=T)) %>%
  ungroup()
d.7 = d.7 %>% na.omit() %>%
  mutate(t.7 = t.7-0.01)
colnames(d.7) = c('group','t','cum')

d8 = data %>% filter(t.8 != 0) %>%
  select(id,date,ret.rm,t.8) %>% group_by(id) %>%
  mutate(cum = cumsum(ret.rm))
p8 = port %>% filter(type=='4.0'&yy=='2018') %>%
  select(id,type,yy,group)
d8 = d8 %>% left_join(p8,by='id')
d.8 = d8 %>% group_by(group,t.8) %>%
  summarise(cum = mean(cum,na.rm=T)) %>%
  ungroup()
d.8 = d.8 %>% na.omit() %>%
  mutate(t.8 = t.8-0.01)
colnames(d.8) = c('group','t','cum')

d9 = data %>% filter(t.9 != 0) %>%
  select(id,date,ret.rm,t.9) %>% group_by(id) %>%
  mutate(cum = cumsum(ret.rm))
p9 = port %>% filter(type=='2.0'&yy=='2019') %>%
  select(id,type,yy,group)
d9 = d9 %>% left_join(p9,by='id')
d.9 = d9 %>% group_by(group,t.9) %>%
  summarise(cum = mean(cum,na.rm=T)) %>%
  ungroup()
d.9 = d.9 %>% na.omit() %>%
  mutate(t.9 = t.9-0.01)
colnames(d.9) = c('group','t','cum')

d10 = data %>% filter(t.10 != 0) %>%
  select(id,date,ret.rm,t.10) %>% group_by(id) %>%
  mutate(cum = cumsum(ret.rm))
p10 = port %>% filter(type=='4.0'&yy=='2019') %>%
  select(id,type,yy,group)
d10 = d10 %>% left_join(p10,by='id')
d.10 = d10 %>% group_by(group,t.10) %>%
  summarise(cum = mean(cum,na.rm=T)) %>%
  ungroup()
d.10 = d.10 %>% na.omit() %>%
  mutate(t.10 = t.10-0.01)
colnames(d.10) = c('group','t','cum')

d11 = data %>% filter(t.11 != 0) %>%
  select(id,date,ret.rm,t.11) %>% group_by(id) %>%
  mutate(cum = cumsum(ret.rm))
p11 = port %>% filter(type=='4.0'&yy=='2020') %>%
  select(id,type,yy,group)
d11 = d11 %>% left_join(p11,by='id')
d.11 = d11 %>% group_by(group,t.11) %>%
  summarise(cum = mean(cum,na.rm=T)) %>%
  ungroup()
d.11 = d.11 %>% na.omit() %>%
  mutate(t.11 = t.11-0.01)
colnames(d.11) = c('group','t','cum')

d12 = data %>% filter(t.12 != 0) %>%
  select(id,date,ret.rm,t.12) %>% group_by(id) %>%
  mutate(cum = cumsum(ret.rm))
p12 = port %>% filter(type=='2.0'&yy=='2021') %>%
  select(id,type,yy,group)
d12 = d12 %>% left_join(p12,by='id')
d.12 = d12 %>% group_by(group,t.12) %>%
  summarise(cum = mean(cum,na.rm=T)) %>%
  ungroup()
d.12 = d.12 %>% na.omit() %>%
  mutate(t.12 = t.12-0.01)
colnames(d.12) = c('group','t','cum')

d13 = data %>% filter(t.13 != 0) %>%
  select(id,date,ret.rm,t.13) %>% group_by(id) %>%
  mutate(cum = cumsum(ret.rm))
p13 = port %>% filter(type=='4.0'&yy=='2021') %>%
  select(id,type,yy,group)
d13 = d13 %>% left_join(p13,by='id')
d.13 = d13 %>% group_by(group,t.13) %>%
  summarise(cum = mean(cum,na.rm=T)) %>%
  ungroup()
d.13 = d.13 %>% na.omit() %>%
  mutate(t.13 = t.13-0.01)

d14 = data %>% filter(t.14 != 0) %>%
  select(id,date,ret.rm,t.14) %>% group_by(id) %>%
  mutate(cum = cumsum(ret.rm))
p14 = port %>% filter(type=='4.0'&yy=='2021') %>%
  select(id,type,yy,group)
d14 = d14 %>% left_join(p14,by='id')
d.14 = d14 %>% group_by(group,t.14) %>%
  summarise(cum = mean(cum,na.rm=T)) %>%
  ungroup()
d.14 = d.14 %>% na.omit() %>%
  mutate(t.14 = t.14-0.01)
colnames(d.14) = c('group','t','cum')

dd = rbind(d.1,d.2,d.3,d.4,d.5,d.6,d.7,d.8,d.9,d.10,d.11,d.12,d.13,d.14)
dd = dd %>% group_by(group,t) %>%
  summarise(cum = mean(cum,na.rm=T)) %>%
  na.omit()
  
##图像绘制
p=ggplot(data=dd,
       aes(x=t,
           y=CAR,
           col=part.port))+
  geom_line() +
  geom_vline(xintercept=0)+
  labs(x='Event time',y='Cumulative abnormal return',
       title='Cumulative abnormal returns by SUE')

# 在图像中画一条在x为0处的垂直虚线
abline(x = 0, lty = "dashed")


   