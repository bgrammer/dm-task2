/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package attributedEmbedding;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

import datautils.Sociopatterns;
import edu.uci.ics.jung.graph.Graph;


public class MixedSpectralMain {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        
    	//To generate synthetic data
//         DataGenerator dg = new DataGenerator();
//       dg.disagreementBetweenGraphAndAttributes();
    	 	
//    	String dataset = "imdb";
//    	String dataset = args[0].toString();
        String dataset = "msrc21"; //"flickr"; //flickr || acm || imdb || dblp || brainA || brainH || karate
		System.out.println("Dataset: " + dataset);


		Sociopatterns sp = new Sociopatterns();
        sp.readData(dataset);
        
        int noG = sp.getG(); //uncomment and specify number of graphs if you use datasets other than BrainNetworks
        int dimensionality = 0;
        int iter = 0;
        int extraiter = 0;
        Graph[] msrc21graphs = null;
        Graph[] measuredDiary = new Graph[noG];
        // we only have 1 graph

        if (dataset.equals("flickr")) {
        	//Flickr set dimensionality to 11 and iter = 30, extraIter = 5
        	measuredDiary[0] = sp.getFlickr0();
        	measuredDiary[1] = sp.getFlickr1();        	
        }
        else if (dataset.equals("acm")) {
        	//ACM - dimensionality = 9 and use all attributes 
        	measuredDiary[0] = sp.getPAP();
	        measuredDiary[1] = sp.getPLP();
        }
		else if (dataset.equals("imdb")) {
			 //IMDB - dimensionality = two(2) and use all attributes 2000 
	        measuredDiary[0] = sp.getMDM();
	        measuredDiary[1] = sp.getMAM();  		        	
		}
		else if (dataset.equals("dblp")) {
			//DBLP 
	        measuredDiary[3] = sp.getdblp0();
	        measuredDiary[1] = sp.getdblp1();
	        measuredDiary[2] = sp.getdblp2();
	        measuredDiary[0] = sp.getdblp3();		
		}
        
		
		else if (dataset.equals("brainA")) {
	        //brain
		    for(int i=0; i<noG; i++) {
		    	measuredDiary[i] = sp.getBrainA(i);
		    }
		    System.out.println("Read Brain Network - Autism");
		    
		}
		else if (dataset.equals("brainH")) {
	        //brain
			for(int i=0; i<noG; i++) {
				measuredDiary[i] = sp.getBrainH(i);
			}
			System.out.println("Read Brain Network - Healthy");
		}
		else if (dataset.equals("karate")) {
			
			measuredDiary[0] = sp.getKarate();
			System.out.println("Read Karate Network");
		}
        
		else if (dataset.equals("synthetic-a")) {
			
			measuredDiary[0] = sp.getGraphA1();
	        measuredDiary[1] = sp.getGraphA1();
			System.out.println("Read Synthetic Data Network - A");
		}
		else if (dataset.equals("msrc21")) {
			msrc21graphs = sp.getMSRC21Graphs();
		}

        //For synthetic dataset
        //measuredDiary[0] = dg.g; 

        int noAtts = sp.getA(); 		//attributes number  
        //int[][] attA = sp.getAllAtt(); 	//if dataset has attributes, get values for all attributes
        //int[][] attA = null; 			//if dataset does not have attributes
                     
        boolean[] weighted = new boolean[noG];
               
        for(int i=0; i<noG; i++) {        
        	weighted[i] = false;            //set if the edges have weights or not
        }
        
        dimensionality = 100; //sp.getDim();
        iter = 50; //sp.getIterations();
        extraiter = 5;// sp.getExtraIter();
      
        System.out.println("Start running, "+dataset+", for dimensionality d = "+dimensionality+".");
        long startTime = System.nanoTime();

        int index = 0;
		for (Graph graph : msrc21graphs) {
			measuredDiary[0] = graph;
			MixedSpectral ms = new MixedSpectral(
					dataset, measuredDiary, weighted, sp.getMSRC21Attrs(index), noAtts, dimensionality, iter, extraiter, sp.getClassId(),index);
			ms.init(0);
			ms.run();
			index++;
		}
	    long endTime = System.nanoTime();
	
	    long duration = (endTime - startTime);  	    	
	    double milisec = duration / 1000000;	    	
	    double sec = milisec / 1000;
	    	
	    System.out.println("Finished for dimensionality = " + String.valueOf(dimensionality));	    	
	    System.out.println("Time = " + sec+" seconds.");
        	
        
    }    
}
