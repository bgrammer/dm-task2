/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package datautils;

import edu.uci.ics.jung.graph.DirectedSparseGraph;
import edu.uci.ics.jung.graph.DirectedSparseMultigraph;
import edu.uci.ics.jung.graph.Graph;
//import jung.graph.Graph;
import edu.uci.ics.jung.graph.Hypergraph;
import edu.uci.ics.jung.graph.UndirectedSparseMultigraph;
import edu.uci.ics.jung.graph.util.EdgeType;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.List;
import java.util.Vector;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import nature.IO;


public class Sociopatterns {

	int[] nodeName;   
    int[][] att;
    int[] classId;
    
    HashMap<Integer, Integer> idToNodeName;
    HashMap<Integer, Integer> nodeNameToId;
    MyNode[] nodes;
    
    static int graphs;
    
    
    //Zachary Karate Club
    Graph karate;
    
    //IMDB
    Graph imdbMDM, imdbMAM;
    
    //ACM
    Graph acmPLP, acmPAP;
    
    //Flickr
    Graph flickrEdge0, flickrEdge1;
     
    //DBLP
    Graph dblp0, dblp1, dblp2, dblp3;
    
    
    Graph s00, s01, s02, s03;
    
    //BrainNet
    Graph brainH, brainA;
    
    //SyntheticData
    Graph g1,g2,g3,g4,g5,g6,g7,g8,g9,g10;
 
    
    static int n = 0; 		//Number of nodes
    static int a = 0; 		//Number of attributes 
    
    static int dim = 0; 	//desired dimensionality
    
    static int iter = 0;
    static int extraiter = 0;
    
    
    
    
    public Sociopatterns() {

    }

    public void readData(String dname) {
    	
    	System.out.println(dname);
    	
    	if(dname.equals("karate")) {
    	//Zachary Karate Club
    		readKarate();
    	}

    	
    	else if(dname.equals("flickr")) {
    		//Flickr
	    	readFlickr0();
	    	readFlickr1();
    	}
    	
    	
    	else if(dname.equals("brainA")) {
    	//brain
    		readBrainA();
    		
    	}
    	
    	else if(dname.equals("brainH")) {
        	//brain
        	readBrainH();
        }
    	
    	else if(dname.equals("imdb")) {
	    	//IMDB
	    	readImdbMDM();
	    	readImdbMAM();
    	}
    	
    	
    	else if(dname.equals("acm")) {
	    	//ACM
	    	readAcmPAP();
	    	readAcmPLP();
    	}
    	
    	
    	else if(dname.equals("dblp")) {
	    	//DBLP:4graphs
	    	readDBLP0();
	    	readDBLP1();
	    	readDBLP2();
	    	readDBLP3();
    	}
    	
    	
    	
    	else if(dname.equals("synthetic-a")) {
	    	//synthetic-a:5A
	    	readGraph1A();
//	    	readGraph2A();
//	    	readGraph3A();
//	    	readGraph4A();
//	    	readGraph5A();
    	}
    	
    	else if(dname.equals("synthetic-g")) {
	    	//synthetic-a:5A
//	    	readGraph2G();
//	    	readGraph4G();
//	    	readGraph6G();
//	    	readGraph8G();
//	    	readGraph10G();
    	}
    	
    	else if(dname.equals("synthetic-n")) {
	    	//synthetic-a:5A
//	    	readGraph2N();
//	    	readGraph4N();
//	    	readGraph6N();
//	    	readGraph8N();
//	    	readGraph10N();
    	}
    	else {
    		System.out.println("Please, check the name of the dataset. It is incorrect!");
    	}
    	
        
    }
    
    
    //Desired dimensionality
    public static int getDim() {
    	return dim;
    }
    
    //Iterations
    public static int getIterations() {
    	return iter;
    }
    
    //Extra iterations
    public static int getExtraIter() {
    	return extraiter;
    }
    
    //Total number of nodes
    public static int getN() {
        return n;
    }
    
    //Total number of attributes
    public static int getA() {
    	return a;
    }
    
    //Values of all node attributes
    public int[][] getAllAtt(){
    	return att;
    }
     
    //Classes (labels) of nodes - we only use them to visualize the graph
    //For this paper we are not focused on visualization, we do not use in this paper(project)
    public int[] getClassId() {
        return classId;
    }
    
    public int getG() {
    	return graphs;	
    }
    
    
    //DBLP - Citation
    public Graph getdblp0() {
    	return dblp0;
    }
    
    //DBLP - CoCitation
    public Graph getdblp1() {
    	return dblp1;
    }
    
    //DBLP - Author-Paper
    public Graph getdblp2() {
    	return dblp2;
    }
    
    //DBLP - CoAuthor
    public Graph getdblp3() {
    	return dblp3;
    }
    
    
    
    //Flickr - Layer0
    public Graph getFlickr0() {
    	return flickrEdge0;
    }
    
    //Flickr - Layer1
    public Graph getFlickr1() {
    	return flickrEdge1;
    }
    

    
    //IMDB - MDM
    public Graph getMDM() {
    	return imdbMDM;
    }
    
    //IMDB - MDM
    public Graph getMAM() {
    	return imdbMAM;
    }
    
    
    //ACM - PLP
    public Graph getPLP() {
    	return acmPLP;
    }
    
    //ACM - PAP
    public Graph getPAP() {
    	return acmPAP;
    }
    
        
    //Zachary Karate Club
    public Graph getKarate() {
    	return karate;
    }
	
    
    //Synthetic Data - A
    public Graph getGraphA1() {
    	return g1;
    }
    
    public Graph getGraphA2() {
    	return g2;
    }

    
    //Reading part of different Graphs and other information, starts from here
    
    
    //BrainNetwork Autism - IDs and Attributes
	public void readBrainA() {

		n = 116;
		a = 5;
		
		String[] pathnames;
        
    	//file path for brain graphs
        File f = new File("data/brainA/a");

        // Populates the array with names of graphs
        pathnames = f.list();
        graphs = pathnames.length;
		
    	IO ea = new IO();
   	 	
    	double[][] dd = ea.readMatlabMatrix("data/brainA/ids.mat", "ids");              

        double[][] at = ea.readMatlabMatrix("data/brainA/Attributes.mat", "data");
                
        idToNodeName = new HashMap<Integer, Integer>();
        nodeNameToId = new HashMap<Integer, Integer>();
        nodes = new MyNode[n];

        att = new int[n][a];
        
        for (int i = 0; i < dd.length; i++) {
            idToNodeName.put((int) dd[i][0], i);
            nodeNameToId.put(i, (int) dd[i][1]);
            nodes[i] = new MyNode(i);
            
            for(int j = 3; j < a; j=j+1){ 	//we do not use the first three attributes(coordinates)
           		 att[i][j] = (int) at[i][j];
            }
        } 
    }
    
	
	//BrainNetwork - IDs and Attributes
		public void readBrainH() {

			n = 116;
			a = 5;
			
			String[] pathnames;
	        
	    	//file path for brain graphs
	        File f = new File("data/brainH/h");

	        // Populates the array with names of graphs
	        pathnames = f.list();
	        graphs = pathnames.length;
			
			
	    	IO ea = new IO();
	   	 	
	    	double[][] dd = ea.readMatlabMatrix("data/brainH/ids.mat", "ids");              

	        double[][] at = ea.readMatlabMatrix("data/brainH/Attributes.mat", "data");
	        	        
	        idToNodeName = new HashMap<Integer, Integer>();
	        nodeNameToId = new HashMap<Integer, Integer>();
	        nodes = new MyNode[n];

	        att = new int[n][a];
	        
	        for (int i = 0; i < dd.length; i++) {
	            idToNodeName.put((int) dd[i][0], i);
	            nodeNameToId.put(i, (int) dd[i][1]);
	            nodes[i] = new MyNode(i);
//	            
	            for(int j = 3; j < a; j=j+1){ 	//we do not use the first three attributes(coordinates)
	           		 att[i][j] = (int) at[i][j];
	           		 }
	        } 
	        
	    }
	
	
	//BrainNetwork - Healthy
	public Graph getBrainH(int graphNo) {
		
		dim = 9;
    	iter = 30;
    	extraiter = 5;
		
		IO ea = new IO();
		
		String[] pathnames;
        
    	//file path for brain graphs
        File f = new File("data/brainH/h");

        // Populates the array with names of graphs
        pathnames = f.list();
        graphs = pathnames.length;
        
        String actualGraph = pathnames[graphNo];
        int l = actualGraph.length();
        
        
        double[][] d = ea.readMatlabMatrix("data/brainH/h/"+actualGraph, actualGraph.substring(0, l-4));
        System.out.println("D length = " + d.length);
        brainH = null;
	    brainH = new UndirectedSparseMultigraph<Integer, MyEdge>();
	    for (int i = 0; i < nodes.length; i++) {
	    	brainH.addVertex(i);
	    }
    
	    int edgeCounter = 0;
	    for (int i = 0; i < d.length; i++) {
   			   brainH.addEdge(new MyEdge(edgeCounter, d[i][2]), ((int) d[i][0]), ((int) d[i][1]), EdgeType.UNDIRECTED);    			   
   			   edgeCounter++;
   	   	}
	    
	    return brainH;
    }
	
	//BrainNetwork - Autism
	public Graph getBrainA(int graphNo) {   	 	
		
		
		dim = 10;
    	iter = 30;
    	extraiter = 5;
		
		IO ea = new IO();
		
    	String[] pathnames;
        
    	//file path for brain graphs
        File f = new File("data/brainA/a");

        // Populates the array with names of graphs
        pathnames = f.list();
        graphs = pathnames.length;
        
        String actualGraph = pathnames[graphNo];
        int l = actualGraph.length();
        
        
        double[][] d = ea.readMatlabMatrix("data/brainA/a/"+actualGraph, actualGraph.substring(0, l-4));
        
        brainA = null;
	    brainA = new UndirectedSparseMultigraph<Integer, MyEdge>();
	    for (int i = 0; i < nodes.length; i++) {
	    	brainA.addVertex(i);
	    }
    
	    int edgeCounter = 0;
	    for (int i = 0; i < d.length; i++) {
   			   brainA.addEdge(new MyEdge(edgeCounter, d[i][2]), ((int) d[i][0]), ((int) d[i][1]), EdgeType.UNDIRECTED);    			   
   			   edgeCounter++;
   	   	}
	    
	    return brainA;
    }
    
	
    
    //IMDB - IDs, Attributes, and MDM graph
   
	public void readImdbMDM() {
    	
		graphs = 2;
		
    	n = 3550;
    	a = 2000;
    	
    	dim = 2;
    	iter = 100;
    	extraiter = 15;
    	
    	IO ea = new IO();
    	
    	double[][] d = ea.readMatlabMatrix("data/imdb/imdb.mat", "MDM");			//MDM graph path
    	double[][] dd = ea.readMatlabMatrix("data/imdb/ids.mat", "ids");            //IDs path
//        double[][] cl = ea.readMatlabMatrix("data/imdb/imdb.mat", "label");			//labels path
        double[][] at = ea.readMatlabMatrix("data/imdb/imdb.mat", "feature");		//feature(attributes) path
        
        idToNodeName = new HashMap<Integer, Integer>();
        nodeNameToId = new HashMap<Integer, Integer>();
        nodes = new MyNode[n];
        classId = new int[n];
        att = new int[n][a];
        
        for (int i = 0; i < dd.length; i++) {
            idToNodeName.put((int) dd[i][0], i);
            nodeNameToId.put(i, (int) dd[i][1]);
            nodes[i] = new MyNode(i);
//            classId[i] = (int) cl[i][0];
            
            for(int j = 0; j < a; j=j+1){
           		 att[i][j] = (int) at[i][j];
            }
        }      
   	
        imdbMDM = new UndirectedSparseMultigraph<Integer, MyEdge>();
       for (int i = 0; i < nodes.length; i++) {
    	   imdbMDM.addVertex(i);
       }

       int edgeCounter = 0;
       for (int i = 0; i < d.length; i++) {
    	   for(int j  = 0; j < d.length; j++) {
    		   if(d[i][j]>0) {
    			   imdbMDM.addEdge(new MyEdge(edgeCounter, d[i][j]),(i), (j), EdgeType.UNDIRECTED);    			   
    			   edgeCounter++;
    	   		}
    		   }
    	   }
       System.out.println("Read IMDB - MDM");
    }
     
    //IMDB - MAM graph
    public void readImdbMAM() {

    	IO ea = new IO();
    	double[][] d = ea.readMatlabMatrix("data/imdb/imdb.mat", "MAM");

    	imdbMAM = new UndirectedSparseMultigraph<Integer, MyEdge>();
    	for (int i = 0; i < nodes.length; i++) {
    		imdbMAM.addVertex(i);
    	}
     
    	int edgeCounter = 0;
    	
    	for (int i = 0; i < d.length; i++) {
    		for(int j  = 0; j < d.length; j++) {
    			if(d[i][j]>0) {
    				imdbMAM.addEdge(new MyEdge(edgeCounter, d[i][j]),(i), (j), EdgeType.UNDIRECTED);    			  
    				edgeCounter++;
    	   		}
    		   }
    	   }
       System.out.println("Read IMDB - MAM");
    }
    
    
    
    
    //Flickr - IDs, and Layer0 graph
    public void readFlickr0() {
    	
    	graphs = 2;
    	
    	n = 9364;
    	a = 0;
    	
    	dim = 11;
    	iter = 30;
    	extraiter = 5;
    	
    	
    	IO ea = new IO();
   	 	
    	double[][] d = ea.readMatlabMatrix("data/flickr/layer0.mat", "layer0");
    	double[][] dd = ea.readMatlabMatrix("data/flickr/ids.mat", "ids");              

        
        idToNodeName = new HashMap<Integer, Integer>();
        nodeNameToId = new HashMap<Integer, Integer>();
        nodes = new MyNode[n];
        
        for (int i = 0; i < n; i++) {
        	
            idToNodeName.put((int) dd[i][0], i);
            nodeNameToId.put(i, (int) dd[i][1]);
            nodes[i] = new MyNode(i);
        	
        }      
   	       
        flickrEdge0 = new UndirectedSparseMultigraph<Integer, MyEdge>();       
        for (int i = 0; i < nodes.length; i++) {    	
        	flickrEdge0.addVertex(i);       
        }
            
        int edgeCounter = 0;
       
        for (int i = 0; i < d.length; i++) {  
        	if(d[i][0] < n && d[i][1] < n  ) {
        		flickrEdge0.addEdge(new MyEdge(edgeCounter, 1.0),((int)(d[i][0])), ((int)(d[i][1])), EdgeType.UNDIRECTED);    			      			   
        		edgeCounter++;    	   
        	}
        }
       
        System.out.println("Read Flickr - Layer 0");
    }
    
    //Flickr - Layer1 graph
    public void readFlickr1() {

    	IO ea = new IO();
   	 	
    	double[][] d = ea.readMatlabMatrix("data/flickr/layer1.mat", "layer1");
       
    	flickrEdge1 = new UndirectedSparseMultigraph<Integer, MyEdge>();
       
    	for (int i = 0; i < nodes.length; i++) {   	   
    		flickrEdge1.addVertex(i);       
    	}     
             
    	int edgeCounter = 0;
       
    	for (int i = 0; i < d.length; i++) {   
    		if(d[i][0] < n && d[i][1] < n  ) {
	    		flickrEdge1.addEdge(new MyEdge(edgeCounter, 1.0),((int)(d[i][0])), ((int)(d[i][1])), EdgeType.UNDIRECTED);    			       			   
	    		edgeCounter++;
    		}
    	}       
    	System.out.println("Read Flickr - Layer 1");
    }
    
    
    
    //ACM - IDs, Attributes, and PAP graph
    public void readAcmPAP() {
    	
    	graphs = 2;
    	
    	n = 3025;
    	a = 1870;
    	
    	dim = 9;
    	iter = 10;
    	extraiter = 2;
    	
    	IO ea = new IO();
   	 	
    	double[][] d = ea.readMatlabMatrix("data/acm/PAP.mat", "PAP");
    	double[][] dd = ea.readMatlabMatrix("data/acm/ids.mat", "ids");              
        double[][] at = ea.readMatlabMatrix("data/acm/feature.mat", "feature");
       
        idToNodeName = new HashMap<Integer, Integer>();
        nodeNameToId = new HashMap<Integer, Integer>();
        nodes = new MyNode[n];
        att = new int[n][a];
        
        
        for (int i = 0; i < dd.length; i++) {
            idToNodeName.put((int) dd[i][0], i);
            nodeNameToId.put(i, (int) dd[i][1]);
            nodes[i] = new MyNode(i);
            
            for(int j = 0; j < a; j=j+1){
           		 att[i][j] = (int) at[i][j];
            }
        }      
   	
       acmPAP = new UndirectedSparseMultigraph<Integer, MyEdge>();
       for (int i = 0; i < nodes.length; i++) {
    	   acmPAP.addVertex(i);
       }
     
       int edgeCounter = 0;
       for (int i = 0; i < d.length; i++) {
    	   for(int j  = 0; j < d.length; j++) {
    		   if(d[i][j]>0) {
    			   acmPAP.addEdge(new MyEdge(edgeCounter, d[i][j]),(i), (j), EdgeType.UNDIRECTED);    			   
    			   edgeCounter++;
    	   		}
    		   }
    	   }
       System.out.println("Read ACM - PAP");
    }
    
    //ACM - PLP (PSP) graph 
    public void readAcmPLP() {

    	IO ea = new IO();
   	 	
    	double[][] d = ea.readMatlabMatrix("data/acm/PLP.mat", "PLP");
  	
    	acmPLP = new UndirectedSparseMultigraph<Integer, MyEdge>();
    	for (int i = 0; i < nodes.length; i++) {
    		acmPLP.addVertex(i);
    	}
     
    	int edgeCounter = 0;
    	for (int i = 0; i < d.length; i++) {
    		for(int j  = 0; j < d.length; j++) {
    			if(d[i][j]>0) {
    				acmPLP.addEdge(new MyEdge(edgeCounter, d[i][j]),(i), (j), EdgeType.UNDIRECTED);    			   
    			    edgeCounter++;
    	   		}
    		}
	   }
       System.out.println("Read ACM - PLP");
    }
    
        
    
    //DBLP - IDs, and Citation graph
    public void readDBLP0() {
    	
    	graphs = 4;
    	
    	n = 8401;
    	a = 0;
    	
    	dim = 2;
    	iter = 50;
    	extraiter = 10;
    	
    	
    	IO ea = new IO();
   	 	
    	double[][] d = ea.readMatlabMatrix("data/dblp/citation.mat", "citation");
    	double[][] dd = ea.readMatlabMatrix("data/dblp/ids.mat", "ids");              

        idToNodeName = new HashMap<Integer, Integer>();
        nodeNameToId = new HashMap<Integer, Integer>();
        nodes = new MyNode[n];
//        classId = new int[n];
        
        for (int i = 0; i < dd.length; i++) {
            idToNodeName.put((int) dd[i][0], i);
            nodeNameToId.put(i, (int) dd[i][1]);
            nodes[i] = new MyNode(i);
        } 
    
        dblp0 = new UndirectedSparseMultigraph<Integer, MyEdge>();
        for (int i = 0; i < nodes.length; i++) {
        	dblp0.addVertex(i);
        }
     
        int edgeCounter = 0;
        for (int i = 0; i < d.length; i++) {
        	if(d[i][2]>0) {
        		dblp0.addEdge(new MyEdge(edgeCounter, d[i][2]),((int)(d[i][0])), ((int)(d[i][1])), EdgeType.UNDIRECTED);    			   
    			edgeCounter++;
        	}
        }
       
        System.out.println("Read DBLP - Citation graph");
    }
    
    //DBLP - Co-Citation graph
    public void readDBLP1() {

    	IO ea = new IO();
   	 	   	
    	double[][] dd = ea.readMatlabMatrix("data/dblp/co_citation.mat", "co_citation");       
        
    	dblp1 = new UndirectedSparseMultigraph<Integer, MyEdge>();
    	for (int i = 0; i < nodes.length; i++) {
    		dblp1.addVertex(i);
    	}
     
    	int edgeCounter = 0;
    	for (int i = 0; i < dd.length; i++) {
    		   	if(dd[i][2]>0) {
    			   dblp1.addEdge(new MyEdge(edgeCounter, dd[i][2]),((int)(dd[i][0])), ((int)(dd[i][1])), EdgeType.UNDIRECTED);    			   
    			   edgeCounter++;
    	   		}    		   
    	}
    	
    	System.out.println("Read DBLP - Co_Citation graph");
    }

    //DBLP - Author-Paper graph
    public void readDBLP2() {

    	IO ea = new IO();
   	 	    	
    	double[][] dd = ea.readMatlabMatrix("data/dblp/APNet.mat", "APNet");
               
    	dblp2 = new UndirectedSparseMultigraph<Integer, MyEdge>();
    	for (int i = 0; i < nodes.length; i++) {
    		dblp2.addVertex(i);
    	}
     
    	int edgeCounter = 0;
    	for (int i = 0; i < dd.length; i++) {
    		if(dd[i][2]>0) {
    			dblp2.addEdge(new MyEdge(edgeCounter, dd[i][2]),((int)(dd[i][0])), ((int)(dd[i][1])), EdgeType.UNDIRECTED);    			   
    			edgeCounter++;
    	   	}
    	}
    	System.out.println("Read DBLP - Authors-Papers graph");
    }
    
    //DBLP - CoAuthor graph
    public void readDBLP3() {
    	
    	IO ea = new IO();
   	 	
    	double[][] dd = ea.readMatlabMatrix("data/dblp/coauthorNet.mat", "coauthorNet");
        
    	dblp3 = new UndirectedSparseMultigraph<Integer, MyEdge>();
    	for (int i = 0; i < nodes.length; i++) {
    		dblp3.addVertex(i);
    	}
     
    	int edgeCounter = 0;
    	for (int i = 0; i < dd.length; i++) {
    		dblp3.addEdge(new MyEdge(edgeCounter, 1.0),((int)(dd[i][0])), ((int)(dd[i][1])), EdgeType.UNDIRECTED);    			   
    		edgeCounter++;
    	}
       
    	System.out.println("Read DBLP - CoAuthor graph");
    }
    
        
    //Zachary Karate Club
    public void readKarate() {
    	
    	graphs = 1;
    	
    	n = 34;
    	a = 0;
    	
    	dim = 3;
    	iter = 30;
    	extraiter = 0;
    	
    	IO ea = new IO();
   	 	
    	double[][] dd = ea.readMatlabMatrix("data/karate/idToFrom.mat", "idToFrom");              
    	double[][] d = ea.readMatlabMatrix("data/karate/Network2.mat", "Network");
        
        idToNodeName = new HashMap<Integer, Integer>();
        nodeNameToId = new HashMap<Integer, Integer>();
        nodes = new MyNode[n];
              
        
        for (int i = 0; i < dd.length; i++) {
            idToNodeName.put((int) dd[i][0], i);
            nodeNameToId.put(i, (int) dd[i][1]);
            nodes[i] = new MyNode(i);
        }      
   	
        karate = new DirectedSparseMultigraph<Integer, MyEdge>();
        for (int i = 0; i < nodes.length; i++) {
        	karate.addVertex(i);
        }
     
       
        int edgeCounter = 0;
        for (int i = 0; i < d.length; i++) {
        	for(int j  = 0; j < d.length; j++) {
        		if(d[i][j]>0) {
    				karate.addEdge(new MyEdge(edgeCounter, d[i][j]),idToNodeName.get((int) i), idToNodeName.get((int) j), EdgeType.DIRECTED);    			   
    				edgeCounter++;
        		}
        	}
        }
    }

    
    public void readGraph1A() {
    	
    	graphs = 2;
    	
    	n = 5000;
    	a = 1000;
    	
    	dim = 3;
    	iter = 50;
    	extraiter = 10;
    	
    	IO ea = new IO();
   	 	
    	String path = "C:/Users/ylli-/Downloads/Spectral Mix/GeneratedData/A/Graph1A.mat";
    	
    	double[][] d0 = ea.readMatlabMatrix(path, "graph0");
    	double[][] d1 = ea.readMatlabMatrix(path, "graph1");
    	double[][] dd = null;
    	for (int i = 1; i <= n; i++) {
    		for (int j = 0; j < 2; j++) {
    			dd[i][j] = (double)i;
    		}
    	}
    	    
    	
    	
        double[][] at = ea.readMatlabMatrix(path, "feature");
       
        idToNodeName = new HashMap<Integer, Integer>();
        nodeNameToId = new HashMap<Integer, Integer>();
        nodes = new MyNode[n];
        att = new int[n][a];
        
        for (int i = 0; i < dd.length; i++) {
            idToNodeName.put((int) dd[i][0], i);
            nodeNameToId.put(i, (int) dd[i][1]);
            nodes[i] = new MyNode(i);
            
            for(int j = 0; j < a; j=j+1){
           		 att[i][j] = (int) at[i][j];
            }
        }      
   	
       g1 = new UndirectedSparseMultigraph<Integer, MyEdge>();
       for (int i = 0; i < nodes.length; i++) {
    	   g1.addVertex(i);
       }
     
       int edgeCounter0 = 0;
       for (int i = 0; i < d0.length; i++) {
    	   for(int j  = 0; j < d0.length; j++) {
    		   if(d0[i][j]>0) {
    			   g1.addEdge(new MyEdge(edgeCounter0, d0[i][j]),(i), (j), EdgeType.UNDIRECTED);    			   
    			   edgeCounter0++;
    	   		}
    		   }
    	   }
       System.out.println("Read Synthetic-A G1");
       
       g2 = new UndirectedSparseMultigraph<Integer, MyEdge>();
       for (int i = 0; i < nodes.length; i++) {
    	   g2.addVertex(i);
       }
     
       int edgeCounter1 = 0;
       for (int i = 0; i < d1.length; i++) {
    	   for(int j  = 0; j < d1.length; j++) {
    		   if(d1[i][j]>0) {
    			   g1.addEdge(new MyEdge(edgeCounter1, d1[i][j]),(i), (j), EdgeType.UNDIRECTED);    			   
    			   edgeCounter1++;
    	   		}
    		   }
    	   }
       System.out.println("Read Synthetic-A G2");
    }
}
