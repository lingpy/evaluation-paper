library("groundhog")
groundhog.day="2021-04-21"
groundhog.library(c('ape', 'maps'), groundhog.day)
source('dependencies/mad.R') # source the mad.R from the file

# Load taxa annotation
tdf = read.csv('taxa-annotation.csv')
tdf$Newlabel<-apply(tdf, 1,function(x) paste0(x[1], ' [',x[4],']'))

# Load the newick trees and change the tip labels
loose = read.tree(file='results/looseid.nwk')
strict = read.tree(file='results/strictid.nwk')
Loose = unroot(loose)
Strict = unroot(strict)
Loose$tip.label= tdf[[5]][match(Loose$tip.label, tdf[[1]])]
Strict$tip.label= tdf[[5]][match(Strict$tip.label, tdf[[1]])]

# Compare unrooted Neighbor, save as a png
pdf(file="plot/loose-strict-unroot.pdf",width = 15, height = 7)
comparePhylo(Loose, Strict, force.rooted=F, plot=T) #first figure
dev.off()

# MAD root
Loose_mad = as.phylo(mad(Loose, 'full')[[6]][[1]])
Strict_mad = as.phylo(mad(Strict, 'full')[[6]][[1]])
Loose_mad$tip.label = replace(Loose_mad$tip.label, Loose_mad$tip.label == "@#Nanjing [M]@#", "Nanjing [M]")

# replace the original Loose and Strict
Loose = Loose_mad
Strict = Strict_mad

# Compare MADrooted trees
pdf(file="plot/loose-strict-root.pdf",width = 20, height = 15)
comparePhylo(Loose, Strict, force.rooted=F, plot=T) # second figure
dev.off()