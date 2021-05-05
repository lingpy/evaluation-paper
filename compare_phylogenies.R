library("groundhog")
groundhog.day = "2021-03-03"
groundhog.library(c('ape','ggplot2', 'reshape2'), groundhog.day)



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
Loose_Coding = read.tree(file='results/part_loose.tre.rooted')
Strict_Coding = read.tree(file='results/part_strict.tre.rooted')
Loose = read.tree(file='results/full_loose.tre.rooted')
Strict = read.tree(file='results/full_strict.tre.rooted')
Sagart = read.tree(file='sagart2005.tre')
Salient = read.tree(file='results/full_salient.tre.rooted')
Common = read.tree(file='results/full_common.tre.rooted')


# Compare MADrooted trees
pdf(file="plots/loose-strict-root.pdf",width = 20, height = 15)
comparePhylo(Loose_Coding, Strict_Coding, force.rooted=F, plot=T) # second figure
dev.off()

# Compare MADrooted trees
pdf(file="plots/sagart-salient.pdf", width=20, height=15)
comparePhylo(Sagart, Salient, force.rooted=F, plot=T) # second figure
dev.off()

# Compare MADrooted trees
pdf(file="plots/sagart-loose.pdf", width=20, height=15)
comparePhylo(Sagart, Loose, force.rooted=F, plot=T) # second figure
dev.off()

# Compare MADrooted trees
pdf(file="plots/salient-strict.pdf", width=20, height=15)
comparePhylo(Salient, Strict, force.rooted=F, plot=T) # second figure
dev.off()

# Compare MADrooted trees
pdf(file="plots/salient-loose.pdf", width=20, height=15)
comparePhylo(Salient, Loose, force.rooted=F, plot=T) # second figure
dev.off()

# Compare MADrooted trees
pdf(file="plots/salient-common.pdf", width=20, height=15)
comparePhylo(Salient, Common, force.rooted=F, plot=T) # second figure
dev.off()






# networks: read delta scores
df = read.csv('results/NN_delta.csv', sep=';')
colnames(df) = c('Taxon', 'Loose','Strict','Salient','Common')
df_melt = melt(df)
pdf(file="plots/delta_score_voilin_plot.pdf",width = 12, height = 9)
p <- ggplot(df_melt, aes(x=variable, y=value, fill=variable)) + 
  geom_violin(trim=FALSE)+
  scale_fill_manual(values=c('#fb8500', '#a8dadc','#ee6c4d','#457b9d'))+
  theme_minimal()+
  labs(x='Full cognate set', y='Delta score')
p+stat_summary(fun.data='mean_sdl',geom='pointrange', color='black')
dev.off()

# test the networks' delta scores
df_aov <- aov(value~variable, data = df_melt)
summary(df_aov)
