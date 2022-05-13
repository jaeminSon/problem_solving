#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>

using namespace std;
int G[128][128];
bool visited[128][128];
int dx[] = {0, 0, -1, 1};
int dy[] = {-1, 1, 0, 0};
int H, W, Q;
int x, y, tc, c;

int main() {
    cin >> H >> W;
	for(int i=0; i<H; i++)
		for(int j=0; j<W; j++){	
			scanf("%d",&G[i][j]);
		}

	cin >> Q;
	for(int i=0; i<Q; i++){
		cin >> x >> y >> c;
		x--;
		y--;
		tc = G[x][y];
		for(int i=0; i<H; i++)
			for(int j=0; j<W; j++)
				visited[i][j] = false;
		vector<vector<int>> pq;
		pq.push_back({x, y});
		while(!pq.empty()){
			vector<int> nc = pq.back();
			pq.pop_back();
			x = nc[0];
			y = nc[1];
			G[x][y] = c;
			for(int i=0; i<4; i++) {
				int nx = x + dx[i];
				int ny = y + dy[i];
				// printf("%d, %d, %d, %d\n", nx, ny, G[nx][ny], visited[nx][ny]);
				if(nx<0 || ny<0 || nx>=H || ny>=W || G[nx][ny]!=tc || visited[nx][ny]) continue;
				visited[nx][ny] = true;
				pq.push_back({nx, ny});
				// printf("here\n");
			}
		}
	}
    
	for(int i=0; i<H; i++){
		for(int j=0; j<W; j++)
			if(j<W-1) printf("%d ",G[i][j]);
			else printf("%d",G[i][j]);
		printf("\n");
	}

}