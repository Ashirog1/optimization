import random
import numpy as np

def datagen(n, r=1, max_distance=100, max_capacity=10):
    l = []
    for i in range(r):
        l.append(random.randint(1, max_capacity))
    z = np.random.randint(low = 1, high = max_distance, size = (2*n+1, 2*n+1))
    for i in range(2*n+1):
        z[i][i] = 0
    
    with open('Data/'+str(n)+'.txt', 'w') as f:
        f.write(str(n)+ ' ')
        for item in l:
            f.write("%s " % item)
        f.write('\n')
        
        for y in z:
            for x in y:
                f.write("%s " % x)
            f.write('\n')
        

if __name__ == '__main__':
    for i in range(5, 100, 5):
        datagen(i)
        
