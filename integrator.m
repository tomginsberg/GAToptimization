Clear;
file = Import["..\\Desktop\\galaxy\\GAToptimization\\trajectory_data.txt", 
   "List"];
solveKepler[x0_, y0_, vx0_, vy0_, t0_, tf_] := 
  Module[{\[Gamma] = 
     39.42}, {{x[t], y[t]} /. 
      NDSolve[{x''[t] + (\[Gamma] (x[t]))/(x[t]^2 + y[t]^2)^(3/2) == 
         0, y''[t] + (\[Gamma] (y[t]))/(x[t]^2 + y[t]^2)^(3/2) == 0, 
        Derivative[1][x][t0] == vx0, x[t0] == x0, 
        Derivative[1][y][t0] == vy0, y[t0] == y0}, {x[t], y[t]}, {t, 
        t0, tf}] // Flatten, t0 <= t < tf}];
pos = ToExpression[file[[1]]]
times = ToExpression[file[[2]]]
vels = ToExpression[file[[3]]]
solution = 
  Table[solveKepler[pos[i][[1]], pos[i][[2]], vels[i][[1]], 
     vels[i][[2]], times[i], times[i + 1]], {i, 1, Length[pos]}] // 
   Piecewise;
Export["..\\Desktop\\galaxy\\GAToptimization\\solarsys\\main\\data\\data.csv", 
  Prepend[Table[
    solution, {t, times[1], times[Length[times]], 0.01}], {y, x}], 
  "CSV"];