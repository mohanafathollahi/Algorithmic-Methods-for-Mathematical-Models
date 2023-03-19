// PLEASE ONLY CHANGE THIS FILE WHERE INDICATED.

int n = ...;
int m = ...;

range V = 1..n;
range W = 1..m;

float G[V][V] = ...; // The matrix is symmetric as the graph is undirected.
float H[W][W] = ...; // The matrix is symmetric as the graph is undirected.

// Define here your decision variables and any other auxiliary data.
// You can run an execute block if needed.
int gX[V][V]; //boolean equivalent of G
int hX[W][W]; //boolean equivalent of H
dvar boolean a[w in W, v in V];
dvar boolean zX[1..m][1..n][1..m][1..n];
dexpr float cost[k in 1..m][l in 1..n][x in 1..m][z in 1..n] = zX[k][l][x][z] * abs(H[k][x] - G[l][z]);


/////////////////////////////////////////////
//PRE
execute {
	for (var i=1;i<=n;i++)
		for (var j=1;j<=n;j++)
			if(G[i][j] != 0.00) gX[i][j] = 1;
			
	for (var i=1;i<=m;i++)
		for (var j=1;j<=m;j++)
			if(H[i][j] != 0.00) hX[i][j] = 1;
}
/////////////////////////////////////////////

minimize // Write here the objective function.
sum (k in 1..m, l in 1..n, x in 1..m, z in 1..n) cost[k][l][x][z] / 2;

subject to {

  // Write here the constraints.    
  forall ( k in 1..m)
	ctFunction:
      sum ( l in 1..n ) a[k][l] == 1;
  
    forall ( l in 1..n)
    ctInjective:
      sum ( k in 1..m ) a[k][l] <= 1;
  
  forall ( k in 1..m)
    forall (l in 1..n)
      forall (x in 1..m)
        forall (z in 1..n)
          ct1:
          	0 <= a[k][l] + a[x][z]  - 2 * zX[k][l][x][z] <= 1;
     
  forall ( k in 1..m)
    forall (l in 1..n)
      forall (x in 1..m)
        forall (z in 1..n)
          ct2:
          	(1 - a[k][l]) + ( 1- a[x][z])  + (hX[k][x] == gX[l][z]) >= 1;    
    
}

execute {
    
    for (var x in W) {
	var fx = 0;
  	for (var u in V) {
  	    if (a[x][u] == 1) fx = u;
    	}
	writeln("f(" + x + ") = " + fx);
    }
}

