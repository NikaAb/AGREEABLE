# BCR GTG

**Automatic generation of ground truth for the evaluation of clonal grouping methods in B-cell populations**

BCR Ground Truth Generator (BCR GTG)  is an automatic method to generate clonal grouping ground truth from real IGH repertoires annotated by IMGT/HighV-QUEST. 

**REFERENCE**  


**CONTACT**  
  E-mail: 
  juliana.silva_bernardes@sorbonne-universite.fr 
  nikaabdollahi@gmail.com 
  
## Inputs
 
  * The IMGT/HighV-QUEST's output in one unzipped folder.
    The following files must be provided:
    * 1_Summary
    * 2_IMGT-gapped
  * See [example input files](https://github.com)

## Outputs

  * Returns
    - 5 tab delimited file:
      * [repertoire_name]\_unannotated_seq.txt : any sequences that could not be annotated fully.
      * [repertoire_name]\_cluster_distribution.txt
      * [repertoire_name]\_initial_clusters_Fo.txt : initial clustering output based on 
      * [repertoire_name]\_final_clusters_Fo.txt : final clustering output
      * [repertoire_name]\_final_clusters_seq_info.txt : each line 

    - A png file containing :

      A) Circle representation of the clone abundance.
      B) Number of sequences in each clone, all clones are represented, vertical axe is in log scale.
      C) Lorenz curve and Gini coefficient.  A Lorenz curve shows the graphical represen-tation of clonal inequality.  On the horizontal axe, it plots the cumulative fraction oftotal clones when ordered from the less to the most abundant; On the vertical axe,it show the cumulative fraction of sequences.
      D) Percentage of the 100 most abundant clone
      * 

  * See [example output files](https://github.com/)  



## Using BCR GTG 
  ```
  In the GTM/Src , run the following command :
  $ bash run_GTM.sh [repertoire_name]

                      
  Output files will be placed as such:
  ~GTM/Src/Output/[repertoire_name]/[repertoire_name]_cluster_distribution.txt
                                    [repertoire_name]_final_clusters_Fo.txt
                                    [repertoire_name]_final_clusters_seq_info.txt
                                    [repertoire_name]_initial_clusters_Fo.txt
                                    [repertoire_name]_unannotated_seq.txt
                                    [repertoire_name]_repertoire.png
  [repertoire_name] is the IMGT/highVquast's output folder name
 ```  
## License, Patches, and Ongoing Developements

  * The program is distributed under the .  
  * [Feature requests and open issues](https://github.com/).

