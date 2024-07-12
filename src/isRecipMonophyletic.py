import pandas as pd
import tskit as tsk

def isRecipMonophyletic(tree, pop_by_node, ancestral) :

    nodes_by_pop = pd.DataFrame(columns=['nodes']) # This will be the list of leaves per population

    for root in tree.roots:
        for leaf in tree.leaves(root):

            current_pop = pop_by_node.loc[leaf, 'pop'] # Get the current leaf's population

            if current_pop != ancestral : # Forget ancestral nodes
                if (current_pop not in nodes_by_pop.index):
                    nodes_by_pop.loc[current_pop] = [[]] # Create a new entry for the population

                nodes_by_pop.at[current_pop, 'nodes'].append(leaf) # Add the leaf to the population
    
    nodes_by_pop['mrca'] = nodes_by_pop['nodes'].apply(lambda x: tree.mrca(*x)) # Identify the MRCA of the population's leaves

    nodes_by_pop['toplevelChildren'] = nodes_by_pop['mrca'].apply(lambda x: list(tree.leaves(x))) # Identify the MRCA's children

    # If each population's MRCA's children are the same as the population's leaves, all populations are reciprocally monophyletic

    return (nodes_by_pop['nodes'] == nodes_by_pop['toplevelChildren']).all()