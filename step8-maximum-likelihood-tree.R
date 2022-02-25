# This step reconstruct maximum likelihood trees first and then the ML network is produced via 1000 iterations. 

# install libraries
 install.packages(c("ape", "phangorn", "pytools"))

library(ape)
library(phangorn)
library(phytools)

# set path 
setwd("nexus")

# likelihood phylogeny
myfun = function(d, outfile){
  tmp = phyDat(read.nexus.data(d), type='USER', levels = c(0,1,'-','?'))
  tre.ini = nj(dist.ml(tmp, model = "F81"))
  fit.ini=pml(tre.ini, tmp, k=2, model = "GTR+I+G")
  fit <- optim.pml(fit.ini, model = "GTR+I+G", optNni=TRUE, optBf=TRUE, optQ=TRUE, optGamma=TRUE,rearrangement="stochastic")
  bs <- bootstrap.pml(fit, bs=1000, optNni=TRUE, multicore=TRUE, mc.cores=1,  control = pml.control(trace = 0))
  svg(file=paste(outfile,'maximum_likelihood_bootstrap.svg', sep=""),width = 15, height = 10)
  plotBS(fit$tree, bs, type='unrooted', method ="TBE", frame="rect")
  outtree = plotBS(fit$tree, bs, type='unrooted', method ="TBE", frame="rect")
  add.scale.bar(length=0.1)
  dev.off()
  print(outtree)
  write.tree(outtree, file=paste(outfile, "tree.tre", sep = "."))
}  

for(d in c("strictid.paps.nex", "looseid.paps.nex", "commonid.paps.nex", "salientid.paps.nex")){
  tmp = phyDat(read.nexus.data(d), type='USER', levels = c(0,1,'-','?'))
  tre.ini = nj(dist.ml(tmp, model = "F81"))
  fit.ini=pml(tre.ini, tmp, k=2, model = "GTR+I+G")
  fit <- optim.pml(fit.ini, model = "GTR+I+G", optNni=TRUE, optBf=TRUE, optQ=TRUE, optGamma=TRUE,rearrangement="stochastic")
  bs <- bootstrap.pml(fit, bs=1000, optNni=TRUE, multicore=TRUE, mc.cores=1,  control = pml.control(trace = 0))
  plotBS(fit$tree, bs, type='phylogram', method ="TBE", frame="rect")
  cnet = consensusNet(bs, p=0.2)
  svg(file=paste(d,'maximum_likelihood_bootstrap_net.svg', sep=""),width = 15, height = 10)
  plot(cnet, show.edge.label = T, col.edge.label = "#FF0000")
  dev.off()
}
  
myfun("strictid.paps.nex", "strict")
myfun("looseid.paps.nex", "loose")
myfun("commonid.paps.nex", "common")
myfun("salientid.paps.nex", "salient")

