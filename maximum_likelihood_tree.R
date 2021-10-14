library(ape)
library(phangorn)

# likelihood phylogeny
myfun = function(d, outfile){
  tmp = phyDat(read.nexus.data(d), type='USER', levels = c(0,1,'-','?'))
  tre.ini <- nj(dist.ml(tmp, model = "F81"))
  fit.ini=pml(tre.ini, tmp, k=2, model = "GTR+I+G")
  fit <- optim.pml(fit.ini, model = "GTR+I+G", optNni=TRUE, optBf=TRUE, optQ=TRUE, optGamma=TRUE)
  bs <- bootstrap.pml(fit, bs=100, optNni=TRUE, multicore=TRUE, mc.cores=1)
  svg(file=paste(outfile,'maximum_likelihood_bootstrap.svg', sep=""),width = 15, height = 10)
  plotBS(fit$tree, bs, type='unrooted')
  outtree = plotBS(fit$tree, bs, type='unrooted')
  add.scale.bar(length=0.1)
  dev.off()
  print(outtree)
  write.tree(outtree, file=paste(outfile, "tree.tre", sep = "."))
}  

myfun("strictid.paps.nex", "strict")
myfun("looseid.paps.nex", "loose")
myfun("commonid.paps.nex", "common")
myfun("salientid.paps.nex", "salient")





