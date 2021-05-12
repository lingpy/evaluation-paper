library("groundhog")
groundhog.day = "2021-05-01"
groundhog.library(c('ape','phangorn', 'ggtree', 'phytools', 'phylotools'), groundhog.day)

library('phangorn')
library('phytools')
# define function

myfun = function(mynexus){
  tmp = phyDat(read.nexus.data(mynexus), type='USER', levels = c(0,1,'-','?'))
  maint = nj(dist.hamming(tmp))
  NJtrees <- bootstrap.phyDat(tmp,
                              FUN=function(x)NJ(dist.hamming(x)), bs=1000)
  treeboot= plotBS(maint, NJtrees, type='unrooted')
  td <- data.frame(matrix(ncol = 2, nrow = treeboot$Nnode))
  colnames(td) = c('nodelabel', 'nodenumber')
  for(i in c(1:treeboot$Nnode)){
    td[i,1]=treeboot$node.label[i]
    td[i,2]=19+i
  }
  td2 = data.frame(matrix(ncol=4, nrow=35))
  colnames(td2) = c('parent', 'child', 'rate', 'tiprate')
  for(i in c(1:nrow(treeboot$edge))){
    tr=td[td$nodenumber==treeboot$edge[i,1],]
    al=tr$nodelabel
    td2[i,]$parent = treeboot$edge[i,1]
    td2[i,]$child = treeboot$edge[i,2]
    td2[i,]$rate = al
    if(treeboot$edge[i, 1] > 19 && treeboot$edge[i, 2]>19){
      td2[i,]$tiprate=NA
    }else{
      td2[i,]$tiprate=al
    }
  }
  treeboot$rate = td2$rate
  treeboot$tiprate =td2$tiprate
  return(treeboot)
}

## files are to be saved as svg, and later, we use other software to convert to pdf. 

# strict
strict_tree = myfun('nexus/strictid.paps.nex')
svg(file='plots/full_strict_branch_support.svg',width = 15, height = 10)
plotBranchbyTrait(strict_tree, strict_tree$rate, mode='edges', type='u', palette = colorRampPalette(c('#0f3d5e','#edfcae','#f50202')),edge.width=7,xlims=c(0,100))
dev.off()

pdf(file='plots/full_strict_branch_support.pdf',width = 15, height = 10)
plotBranchbyTrait(strict_tree, strict_tree$rate, mode='edges', type='u', palette = colorRampPalette(c('#0f3d5e','#edfcae','#f50202')),edge.width=7,xlims=c(0,100))
dev.off()

# loose
loose_tree = myfun('nexus/looseid.paps.nex')
svg(file='plots/full_loose_branch_support.svg',width =15, height = 10)
plotBranchbyTrait(loose_tree,loose_tree$rate, mode='edges', type='u', palette = colorRampPalette(c('#0f3d5e','#edfcae','#f50202')),edge.width=7,xlims=c(0,100))
dev.off()

pdf(file='plots/full_loose_branch_support.pdf',width =15, height = 10)
plotBranchbyTrait(loose_tree,loose_tree$rate, mode='edges', type='u', palette = colorRampPalette(c('#0f3d5e','#edfcae','#f50202')),edge.width=7,xlims=c(0,100))
dev.off()

# common
common_tree = myfun('nexus/commonid.paps.nex')
svg(file='plots/full_common_branch_support.svg',width = 15, height = 10)
plotBranchbyTrait(common_tree,common_tree$rate, mode='edges', type='u', palette = colorRampPalette(c('#0f3d5e','#edfcae','#f50202')),edge.width=7,xlims=c(0,100))
dev.off()

pdf(file='plots/full_common_branch_support.pdf',width = 15, height = 10)
plotBranchbyTrait(common_tree,common_tree$rate, mode='edges', type='u', palette = colorRampPalette(c('#0f3d5e','#edfcae','#f50202')),edge.width=7,xlims=c(0,100))
dev.off()

# salient
salient_tree = myfun('nexus/salientid.paps.nex')
svg(file='plots/full_salient_branch_support.svg',width = 15, height = 10)
plotBranchbyTrait(salient_tree,salient_tree$rate, mode='edges', type='u', palette = colorRampPalette(c('#0f3d5e','#edfcae','#f50202')),edge.width=7,xlims=c(0,100))
dev.off()

pdf(file='plots/full_salient_branch_support.pdf',width = 15, height = 10)
plotBranchbyTrait(salient_tree,salient_tree$rate, mode='edges', type='u', palette = colorRampPalette(c('#0f3d5e','#edfcae','#f50202')),edge.width=7,xlims=c(0,100))
dev.off()


