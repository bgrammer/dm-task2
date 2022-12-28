Our source code is implemented in Java and Python.
Java is used for main part of the paper and we have used Python to run KMeans on node embeddings obtained from SpectralMix and other methods too. 

1. Java code is available here. Main class is MixedSpectralMain(package attributedEmbedding).
To run the code: java jar -SpectralMix.jar datasetName 
for example: java -jar SpectralMix.jar flickr


2. Some parameters can be changed on MixedSpectralMain.java (package attributedEmbedding) , Sociopatterns.java (package datautil), and MixedSpectral.java (package attributedEmbedding) classes.
3. Parameters for synthetic datasets can be changed on DataGenerator.java and DataGeneratorMain.java classes.

Datasets are stored in folder data.
Embeddings will be stored in folder embeddings.

4. To run KMeans on the final embeddings run the code on the KMeans python notebook. 