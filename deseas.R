library(forecast)
library(xts)
dates<-seq(as.POSIXct('2012-01-01 00:00',tz='UTC'),length=365*8+2,by="hour")
files<-Sys.glob("gun_data/raw/*.np", dirmark = FALSE)
for (fname in files){
	df<-data.frame(read.table(fname)$V1[1:(365*8+2)])
	xt<-xts(x=df, order.by=dates[1:nrow(df)])
	Z1<-apply.weekly(xt,sum)
	M1<-(mstl(msts(Z1,seasonal.period=c(365.25/7,365.25/12/7))))
	r1<-M1[1:nrow(M1),ncol(M1)]
	write.csv(r1,paste(fname,".weekly.detrend.csv",sep=""))
	write.csv(M1,paste(fname,".weekly.decomp.csv",sep=""))
	xt2<-xts(x=df, order.by=dates[1:nrow(df)])
	M2<-(mstl(msts(xt2,seasonal.period=c(7,365.25/12,365.25))))
	r2<-M2[1:nrow(M2),ncol(M2)]
	write.csv(r2,paste(fname,".daily.detrend.csv",sep=""))
	write.csv(M2,paste(fname,".daily.decomp.csv",sep=""))
}
