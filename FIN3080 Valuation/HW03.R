library(dplyr)
library(readxl)
library(moments)

month = read_xlsx('C:/Users/任自芃/Desktop/data/MONTH.xlsx')
month = month[-1:-2,]
month$ChangeRatio = as.numeric(month$ChangeRatio)
week = read_xlsx('C:/Users/任自芃/Desktop/data/WEEK.xlsx')
week = week[-1:-2,]
week$ChangeRatio = as.numeric(week$ChangeRatio)
day1 = read_xlsx('C:/Users/任自芃/Desktop/data/DAY1.xlsx')
day1 = day1[-1:-2,]
day2 = read_xlsx('C:/Users/任自芃/Desktop/data/DAY2.xlsx')
day2 = day2[-1:-2,]
day = rbind(day1,day2)
day$ChangeRatio = as.numeric(day$ChangeRatio)
day = day %>% filter(ChangeRatio!=0)

month_1 = month %>% filter(Symbol=='000300')
mean(month_1$ChangeRatio)
sd(month_1$ChangeRatio)^2
skewness(month_1$ChangeRatio)
kurtosis(month_1$ChangeRatio)
shapiro.test(month_1$ChangeRatio)
agostino.test(month_1$ChangeRatio)
anscombe.test(month_1$ChangeRatio)
hist(month_1$ChangeRatio,breaks=10,main="CSI300月数据",
     labels=F,col="blue",border="red",freq=T,xlab = '月回报',ylab = '频数')
lines(density(month_1$ChangeRatio),col='black',lwd=2)
legend('topleft',legend = c('拟合分布曲线'),col = c('black'), lty = 1,lwd = 2)
ggqqplot(month_1$ChangeRatio,color = 'blue',main='CSI300月数据',xlab = '理论分位数', ylab = '样本分位数')

week_1 = week %>% filter(Symbol=='000300')
mean(week_1$ChangeRatio)
sd(week_1$ChangeRatio)^2
skewness(week_1$ChangeRatio)
kurtosis(week_1$ChangeRatio)
shapiro.test(week_1$ChangeRatio)
agostino.test(week_1$ChangeRatio)
anscombe.test(week_1$ChangeRatio)
hist(week_1$ChangeRatio,breaks=50,main="CSI300周数据",
     labels=F,col="blue",border="red",freq=T,xlab = '周回报',ylab = '频数')
lines(density(week_1$ChangeRatio),col='black',lwd=2)
legend('topleft',legend = c('拟合分布曲线'),col = c('black'), lty = 1,lwd = 2)
ggqqplot(week_1$ChangeRatio,color = 'blue',main='CSI300周数据',xlab = '理论分位数', ylab = '样本分位数')

day_1 = day %>% filter(Symbol=='000300')
mean(day_1$ChangeRatio)
sd(day_1$ChangeRatio)^2
skewness(day_1$ChangeRatio)
kurtosis(day_1$ChangeRatio)
shapiro.test(day_1$ChangeRatio)
agostino.test(day_1$ChangeRatio)
anscombe.test(day_1$ChangeRatio)
hist(day_1$ChangeRatio,breaks=200,main="CSI300日数据",
     labels=F,col="blue",border="red",freq=T,xlab = '日回报',ylab = '频数')
lines(density(day_1$ChangeRatio),col='black',lwd=2)
legend('topleft',legend = c('拟合分布曲线'),col = c('black'), lty = 1,lwd = 2)
ggqqplot(day_1$ChangeRatio,color = 'blue',main='CSI300日数据',xlab = '理论分位数', ylab = '样本分位数')





month_2 = month %>% filter(Symbol=='399006')
mean(month_2$ChangeRatio)
sd(month_2$ChangeRatio)^2
skewness(month_2$ChangeRatio)
kurtosis(month_2$ChangeRatio)
shapiro.test(month_2$ChangeRatio)
agostino.test(month_2$ChangeRatio)
anscombe.test(month_2$ChangeRatio)
hist(month_2$ChangeRatio,breaks=10,main="GEI月数据",
     labels=F,col="blue",border="red",freq=T,xlab = '月回报',ylab = '频数')
lines(density(month_2$ChangeRatio),col='black',lwd=2)
legend('topleft',legend = c('拟合分布曲线'),col = c('black'), lty = 1,lwd = 2)
ggqqplot(month_2$ChangeRatio,color = 'blue',main='GEI月数据',xlab = '理论分位数', ylab = '样本分位数')

week_2 = week %>% filter(Symbol=='399006')
mean(week_2$ChangeRatio)
sd(week_2$ChangeRatio)^2
skewness(week_2$ChangeRatio)
kurtosis(week_2$ChangeRatio)
shapiro.test(week_2$ChangeRatio)
agostino.test(week_2$ChangeRatio)
anscombe.test(week_2$ChangeRatio)
hist(week_2$ChangeRatio,breaks=50,main="GEI周数据",
     labels=F,col="blue",border="red",freq=T,xlab = '周回报',ylab = '频数')
lines(density(week_2$ChangeRatio),col='black',lwd=2)
legend('topleft',legend = c('拟合分布曲线'),col = c('black'), lty = 1,lwd = 2)
ggqqplot(week_2$ChangeRatio,color = 'blue',main='GEI周数据',xlab = '理论分位数', ylab = '样本分位数')

day_2 = day %>% filter(Symbol=='399006')
mean(day_2$ChangeRatio)
sd(day_2$ChangeRatio)^2
skewness(day_2$ChangeRatio)
kurtosis(day_2$ChangeRatio)
shapiro.test(day_2$ChangeRatio)
agostino.test(day_2$ChangeRatio)
anscombe.test(day_2$ChangeRatio)
hist(day_2$ChangeRatio,breaks=200,main="GEI日数据",
     labels=F,col="blue",border="red",freq=T,xlab = '日回报',ylab = '频数')
lines(density(day_2$ChangeRatio),col='black',lwd=2)
legend('topleft',legend = c('拟合分布曲线'),col = c('black'), lty = 1,lwd = 2)
ggqqplot(day_2$ChangeRatio,color = 'blue',main='GEI日数据',xlab = '理论分位数', ylab = '样本分位数')
