#include<bits/stdc++.h>
using namespace std;

vector<int> f(int n){
    vector<int> a(5,0);
    // for(int i=0;i<5;i++){
    //     a[i] = 0;
    // }
    if(n/5 ==1){
        a[4] = 1;
    }
    int x = n%5;
    for(int i=x-1;i>=0;i--){
        a[i] = 1;
    }
    return a;
}


int main(){
    int n;cin>>n;
    if(n>99 || n<0){
        cout<<"Invalid input\n";
    }else{
        int rn = n%10;
        int ln = n/10;
    
        vector<int> l = f(ln);
        vector<int> r = f(rn);
        for(int i=0;i<5;i++){
            cout<<l[i]<<" ";
        }
        for(int i=4;i>=0;i--){
            cout<<r[i]<<" ";
        }
        cout<<endl; 
        
    }
    return 0;
}