#############################################################
## Reconstruct maximum likelihood (ML) trees and networks.
#############################################################

#checking the environment
for(p in c("ape", "phangorn", "phytools")){
  if(!p %in% installed.packages()){
    install.packages(p)
  }
}

# import libraries and set the working path
library(ape)
library(phangorn)
library(phytools)
setwd('bayes/')

# functions to generate maximum likelihood trees
generate_ml = function(d, outfile_name){
  tmp = phyDat(read.nexus.data(d), type='USER', levels = c(0,1,'-','?'))
  tre.ini = nj(dist.ml(tmp, model = "F81"))
  fit.ini = pml(tre.ini, tmp, k=2, model = "GTR+I+G")
  fit = optim.pml(fit.ini, model = "GTR+I+G", optNni=TRUE, optBf=TRUE, optQ=TRUE, optGamma=TRUE,rearrangement="stochastic")
  print("bootstrapping...")
  bs = bootstrap.pml(fit, bs=1000, optNni=TRUE, multicore=TRUE, mc.cores=1,  control = pml.control(trace = 0))
  print("done bootstrapping.")
  print("print ML tree to file")
  svg(file=paste(outfile_name,'ml-tree.svg', sep="-"),width = 15, height = 10)
  outtree = plotBS(fit$tree, bs, type='unrooted', method ="TBE", frame="rect")
  add.scale.bar(length=0.1)
  dev.off()
  print("print ML network to file")
  svg(file=paste(outfile_name,'ml-net.svg', sep="-"),width = 15, height = 10)
  cnet = consensusNet(bs, p=0.2)
  plot(cnet, show.edge.label = T, col.edge.label = "#FF0000")
  dev.off()
  print("done")
}
  
for(d in c(
  'part-strictid.nex', 
  'part-looseid.nex', 
  'part-commonid.nex', 
  'part-salientid.nex',
  'full-strictid.nex',
  'full-looseid.nex',
  'full-commonid.nex',
  'full-salientid.nex')
  ){
  sprintf("processing % s", d)
  output_filename = gsub(".nex", "-plot", d)
  generate_ml(d, output_filename)
}

