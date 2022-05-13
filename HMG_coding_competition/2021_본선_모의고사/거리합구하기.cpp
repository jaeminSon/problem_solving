#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>

using namespace std;
vector<vector<vector<unsigned int>>> G;
bool visited[200000];
unsigned int N;
unsigned int s, e, t;
unsigned long total_dist;
unsigned long dist;
unsigned int curr, child, edge_dist;

int main() {
    cin >> N;
	if(N == 1){
		printf("0\n");
	}
	else{
		for(int i=0; i<N; i++){
			vector<vector<unsigned int>> new_vector;
			G.push_back(new_vector);
		}

		for(int i=0; i<N-1; i++){
			scanf("%d", &s);
			scanf("%d", &e);
			scanf("%d", &t);
			G[s-1].push_back({e-1, t});
			G[e-1].push_back({s-1, t});
		}

		for(int i=0; i<N; i++){

			total_dist = 0;
			
			for(int t=0; t<N; t++)
				visited[t] = false;
			
			vector<vector<unsigned int>> pq;
			pq.push_back({i, 0});
			visited[i] = true;
			while(!pq.empty()){
				vector<unsigned int> nc = pq.back();
				pq.pop_back();
				curr = nc[0];
				dist = nc[1];
				// printf("%d, %d, %lu \n", curr, dist, total_dist);
				total_dist += dist;
				for(s=0; s < G[curr].size(); s++){
					child = G[curr][s][0];
					if(!visited[child]){
						visited[child] = true;
						edge_dist = G[curr][s][1];
						pq.push_back({child, dist + edge_dist});
					}
				}
			}
			printf("%lu\n", total_dist);
		}
	}
}