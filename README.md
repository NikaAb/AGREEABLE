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
  * See [example input files](https://github.com/NikaAb/BCR_GTG/tree/master/Database/IMGT_highvquest_output)

## Outputs

  * BCR GTG returns:

    - 5 tab delimited file:

      * [repertoire_name]\_unannotated_seq.txt : any sequences that could not be annotated fully. [example](https://github.com/NikaAb/BCR_GTG/blob/master/Database/GTM_output/I1_IMGT/I1_IMGT_unannotated_seq.txt)

      The columns are:
      ```
      seq Id   functionality  IGHV_and_allele IGHJ_and_allele CDR3
      ```
      * [repertoire_name]\_cluster_distribution.txt : clusters and their abundance sorted from highest to lowest.[example](https://github.com/NikaAb/BCR_GTG/blob/master/Database/GTM_output/I1_IMGT/I1_IMGT_cluster_distribution.txt)

      The columns are:
      ```
      cluster_Id   abundance
      ```

      * [repertoire_name]\_initial_clusters_Fo.txt : initial clustering output. Sequences with the same IGHV and IGHJ genes, same CDR3 sequence length, and CDR3 identity higher than 70% are grouped together.[example](https://github.com/NikaAb/BCR_GTG/blob/master/Database/GTM_output/I1_IMGT/I1_IMGT_initial_clusters_Fo.txt)

      Each line contains the one cluster id and all the sequence ids of it's members.
      ```
      cluster_Id   seqid1 seqid2 ...
      ```
      * [repertoire_name]\_final_clusters_Fo.txt : final clustering output, after minimizing intraclonal distances and maximizing interclonal distances.[example](https://github.com/NikaAb/BCR_GTG/blob/master/Database/GTM_output/I1_IMGT/I1_IMGT_final_clusters_Fo.txt)
      ```
      cluster_Id   seqid1 seqid2 ...
      ```
      * [repertoire_name]\_final_clusters_seq_info.txt : each line contains the following information for each sequence:
      ```
      Cluster_id__clonotype_id   seq Id  functionality  IGHV_and_allele IGHJ_and_allele CDR3 Junction
      ```
          [example](https://github.com/NikaAb/BCR_GTG/blob/master/Database/GTM_output/I1_IMGT/I1_IMGT_final_clusters_seq_info.txt)

    - A png file containing:

      ![alt text](https://github.com/NikaAb/BCR_GTG/blob/master/Database/GTM_output/I1_IMGT/I1_IMGT_repertoire.png "Title Text")

      A) Circle representation of the clone abundance.Each  circle  symbolizes  a  clone,and the clone’s abundance is shown through its size.

      B) Number of sequences in each clone, all clones are represented, vertical axe is in log scale.

      C) Lorenz curve and Gini coefficient. A Lorenz curve shows the graphical represen-tation of clonal inequality. On the horizontal axe, it plots the cumulative fraction oftotal clones when ordered from the less to the most abundant; On the vertical axe,it show the cumulative fraction of sequences.

      D) Percentage of the 100 most abundant clones.
       



## Using BCR GTG 
  In the GTM/Src , run the following command:
  ```
  $ bash run_GTM.sh [repertoire_name]
  ```
                      
  Output files will be placed as such:
  ```
  ~GTM/Src/Output/[repertoire_name]/[repertoire_name]_cluster_distribution.txt
                                    [repertoire_name]_final_clusters_Fo.txt
                                    [repertoire_name]_final_clusters_seq_info.txt
                                    [repertoire_name]_initial_clusters_Fo.txt
                                    [repertoire_name]_unannotated_seq.txt
                                    [repertoire_name]_repertoire.png
 ```
 [repertoire_name] is the IMGT/highVquast's output folder name.
## License, Patches, and Ongoing Developements

  * The program is distributed under the .  
  * [Feature requests and open issues](https://github.com/NikaAb/BCR_GTG/issues).

