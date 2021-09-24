#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct Data{
    int x,y,xx,yy;
    int isHorizontal;
    int wallPosition;
    int spacePosition;
    int last;
} Data;

typedef struct Node{
    struct Data val;
    struct Node* left;
    struct Node* right;
} Node ;
typedef struct Path{
  int x;
  int y;
  struct Path* next;
}Path;

struct Node* CreateMazeTree(int x,int xx,int y , int yy){
    if(x<0 || xx <0 || y<0 || yy<0 || x>xx || y>yy)
      return NULL;
    struct Node* obj = malloc(sizeof(struct Node));
    obj->val.x=x;
    obj->val.xx=xx;
    obj->val.y=y;
    obj->val.yy=yy;
    if(xx-x==0 && yy-y==0){
        obj->val.last = 1;
    }else{
      obj->val.last = 0;
      obj->val.isHorizontal= rand()%2;
      if(obj->val.isHorizontal==1 && (yy-y)==0){
        obj->val.isHorizontal=0;
      }else if (obj->val.isHorizontal==0 && (xx-x)==0){
        obj->val.isHorizontal=1;
      }
      if(obj->val.isHorizontal){
          obj->val.wallPosition=(yy+y)/2;
          obj->val.spacePosition=(((xx-x)==0)?(x):(rand()%(xx-x)+x));
          obj->left=CreateMazeTree(x,xx,y,obj->val.wallPosition);
          obj->right=CreateMazeTree(x,xx,obj->val.wallPosition+1,yy);
      }else{
          obj->val.wallPosition=(xx+x)/2;
          obj->val.spacePosition=(((yy-y)==0)?(y):(rand()%(yy-y)+y));
          obj->left=CreateMazeTree(x,obj->val.wallPosition,y ,yy);
          obj->right=CreateMazeTree(obj->val.wallPosition+1,xx,y ,yy);
      }
    }
    return obj;
}

void freeNode(struct Node* obj){
    srand(time(NULL));
    if(!obj->val.last){
      freeNode(obj->left);
      freeNode(obj->right);
    }
    free(obj);
}
int k;
struct Path* getPath(struct Node* a ,int x,int y,int pp,int pd){
  struct Path* path=malloc(sizeof(struct Path));
  if(a->val.last ){
    path->x=a->val.x;
    path->y=a->val.y;
  }else if (a->val.isHorizontal){
    path->x=a->val.spacePosition;
    path->y=a->val.wallPosition;
    if(a->right && y>=a->right->val.y && y<=a->right->val.yy && x>=a->right->val.x && x<=a->right->val.xx)
      if((pd==1 && pp>=a->right->val.y && pp<=a->right->val.yy)||(pd==0 && pp>=a->right->val.x && pp<=a->right->val.xx))
        path = getPath(a->right ,x,y,a->val.spacePosition,a->val.isHorizontal);
      else
        path->next = getPath(a->right ,x,y,a->val.spacePosition,a->val.isHorizontal);
    else if(a->left && y>=a->left->val.y && y<=a->left->val.yy  && x>=a->left->val.x && x<=a->left->val.xx)
      if((pd==1 && pp>=a->left->val.y && pp<=a->left->val.yy)||(pd==0 && pp>=a->left->val.x && pp<=a->left->val.xx))
        path = getPath(a->left ,x,y,a->val.spacePosition,a->val.isHorizontal);
      else
        path->next = getPath(a->left ,x,y,a->val.spacePosition,a->val.isHorizontal);
  }else{
    path->y=a->val.spacePosition;
    path->x=a->val.wallPosition;
    if(a->right && y>=a->right->val.y && y<=a->right->val.yy && x>=a->right->val.x && x<=a->right->val.xx)
      if((pd==1 && pp>=a->right->val.y && pp<=a->right->val.yy)||(pd==0 && pp>=a->right->val.x && pp<=a->right->val.xx))
        path = getPath(a->right ,x,y,a->val.spacePosition,a->val.isHorizontal);
      else
        path->next = getPath(a->right ,x,y,a->val.spacePosition,a->val.isHorizontal);
    else if(a->left&& y>=a->left->val.y && y<=a->left->val.yy  && x>=a->left->val.x && x<=a->left->val.xx)
      if((pd==1 && pp>=a->left->val.y && pp<=a->left->val.yy)||(pd==0 && pp>=a->left->val.x && pp<=a->left->val.xx))
        path = getPath(a->left ,x,y,a->val.spacePosition,a->val.isHorizontal);
      else
        path->next = getPath(a->left ,x,y,a->val.spacePosition,a->val.isHorizontal);
  }
  return path;
}
struct Path* getFullPath(struct Node* a ,int x,int y,int xx,int yy){
  struct Path* tmp;
  struct Path* start;
  start = getPath(a,x,y,-1,-1);
  struct Path* end;
  end = getPath(a,xx,yy,-1,-1);
  tmp=start;
  while(start->next && end->next && start->next->x==end->next->x && start->next->y==end->next->y ){
    start=start->next;
    end=end->next;
  }
  while(tmp->next!=NULL){
      tmp=tmp->next;
    }
  tmp->next=end;
  return start;
}
void generateTabelFromTree(struct Node* a ,char*** t){
  if(a->val.isHorizontal){
    for(int i = 2*a->val.x+1;i<2*(a->val.xx+1);i++){
      (*t)[2*(a->val.wallPosition+1)][i]='#';
    }
    (*t)[2*(a->val.wallPosition+1)][2*a->val.spacePosition+1]=' ';
  }else{
    for(int i = 2*(a->val.y+1);i<2*(a->val.yy+1);i++){
        (*t)[i][2*(a->val.wallPosition+1)]='#';
    }
      (*t)[2*a->val.spacePosition+1][2*(a->val.wallPosition+1)]=' ';

    k++;
  }
  if(!a->val.last){
    generateTabelFromTree(a->left ,t);
    generateTabelFromTree(a->right ,t);
  }
}

void addPathToTheTabel(struct Path* path,char*** t){
  while(path->next!=NULL){
    (*t)[2*path->y+1][2*path->x+1]='@';
    path=path->next;
  }
}


int main(int argc, char const *argv[]){
    int n=50,m=20;
    k=0;
    srand(getpid());
    struct Node* tree=CreateMazeTree(0,m-1,0,n-1);
    char** tabel;
    tabel = malloc(sizeof(char*)*(2*n+1));
    for(int i = 0;i<2*n+1;i++){
      tabel[i] = malloc(sizeof(char)*(2*m+1));
      for(int j  = 0;j<2*m+1;j++){
        tabel[i][j]=' ';
        if (i==0 || j==0 || i==2*n || j==2*m)
          tabel[i][j]='#';
      }
    }
    struct Path* path;
    generateTabelFromTree(tree,&tabel);
    path = getFullPath(tree,0,0,m-1,n-1);
    addPathToTheTabel(path,&tabel);
    //print tabel
    for(int i = 1;i<2*n+1;i+=2){
      for(int j = 1;j<2*m+1;j+=2){
        char* bottom = tabel[i + 1][j];
        char* right = tabel[i][j + 1];
        if (bottom == ' ' && right == ' ') {
            printf("%d", 0);
        } else if (bottom == ' ' && right == '#') {
            printf("%d", 1);
        } else if (bottom == '#' && right == ' ') {
            printf("%d", 2);
        } else {
            printf("%d", 3);
        }
      }
      printf("\n");
    }
    for(int i = 0;i<2*n+1;i++){
      for(int j  = 0;j<2*m+1;j++){
        //printf("%c",tabel[i][j]);
      }
      //printf("\n");
      free(tabel[i]);
    }
    freeNode(tree);
    return 0;
}
