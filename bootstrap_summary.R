library("groundhog")
groundhog.day = "2021-05-01"
groundhog.library(c('ape','phangorn', 'ggtree', 'phytools', 'phylotools'), groundhog.day)
source('dependencies/mad.R')

# define function

myfun = function(main, random){
  main_tree = read.tree(main)
  main_tree = read.newick(text=mad(main_tree, 'newick'))
  random_tree = read.tree(random)
  for(i in c(1:length(random_tree))){
    tmp = read.tree(text=mad(random_tree[[i]],'newick'))
    if(class(tmp)=='phylo'){
      random_tree[[i]]=tmp
    }else{
      random_tree[[i]]=tmp[[1]]
    }
  }
  sum_tree = plotBS(main_tree, random_tree, 'phylogram')
  return(sum_tree)
}


# strict
strict_tree = myfun('results/full_strict.tre', 'results/full_random_trees_strict.tre')
pdf(file='plots/full_strict_branch_support.pdf',width = 24, height = 10)
ggtree(strict_tree)+geom_text(aes(label=label, vjust=0.3, hjust=-0.1))+theme_tree2()
dev.off()

# loose
loose_tree = myfun('results/full_loose.tre', 'results/full_random_trees_loose.tre')
pdf(file='plots/full_loose_branch_support.pdf',width = 24, height = 10)
ggtree(loose_tree)+geom_text(aes(label=label, vjust=0.3, hjust=-0.1))+theme_tree2()
dev.off()

# common
common_tree = myfun('results/full_common.tre', 'results/full_random_trees_common.tre')
pdf(file='plots/full_common_branch_support.pdf',width = 24, height = 10)
ggtree(common_tree)+geom_text(aes(label=label, vjust=0.3, hjust=-0.1))+theme_tree2()
dev.off()

# salient
salient_tree = myfun('results/full_salient.tre', 'results/full_random_trees_salient.tre')
pdf(file='plots/full_salient_branch_support.pdf',width = 24, height = 10)
ggtree(salient_tree)+geom_text(aes(label=label, vjust=0.3, hjust=-0.1))+theme_tree2()
dev.off()