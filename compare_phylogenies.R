library("groundhog")
groundhog.day="2021-04-21"
groundhog.library('ape', groundhog.day)

# Load the newick trees and change the tip labels
loose = read.tree(file='results/part_loose.tre')
strict = read.tree(file='results/part_strict.tre')
Loose = unroot(loose)
Strict = unroot(strict)


# Compare unrooted Neighbor, save as a png
pdf(file="plots/loose-strict-unroot.pdf",width = 20, height = 8)
comparePhylo(Loose, Strict, force.rooted=F, plot=T) #first figure
dev.off()

# MAD root
Loose_mad = read.tree(file='results/part_loose.tre.rooted')
Strict_mad = read.tree(file='results/part_strict.tre.rooted')

# Compare MADrooted trees
pdf(file="plots/loose-strict-root.pdf",width = 20, height = 15)
comparePhylo(Loose_mad, Strict_mad, force.rooted=F, plot=T) # second figure
dev.off()