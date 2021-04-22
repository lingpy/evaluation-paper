library('ape')
library('phytools')
library("colorspace")
source("../../mad/mad.R") # source the script from the file

# Load the grouping, create the labels for tip taxa
Tdf = read.csv('tipShape.csv')
Tdf$Newlabel<-apply(Tdf, 1,function(x) paste0(x[1], ' [',x[4],']'))

# Load the newick trees and change the tip labels
loose = read.tree(file='looseid.nwk')
strict = read.tree(file='strictid.nwk')
Loose = unroot(loose)
Strict = unroot(strict)
Loose$tip.label= Tdf[[5]][match(Loose$tip.label, Tdf[[1]])]
Strict$tip.label= Tdf[[5]][match(Strict$tip.label, Tdf[[1]])]

# Compare unrooted Neighbor
comparePhylo(Loose, Strict, force.rooted=F, plot=T)

# MAD root
Loose_mad = as.phylo(mad(Loose, 'full')[[6]][[1]])
Strict_mad = as.phylo(mad(Strict, 'full')[[6]][[1]])
Loose_mad$tip.label = replace(Loose_mad$tip.label, Loose_mad$tip.label == "@#Nanjing [M]@#", "Nanjing [M]")

# replace the original Loose and Strict
Loose = Loose_mad
Strict = Strict_mad

# Compare MADrooted trees
comparePhylo(Loose, Strict, force.rooted=F, plot=T)
