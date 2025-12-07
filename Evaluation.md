# Evaluation



#### Throughput



Under one second interval makes the page flicker constantly and occasionally crashes.



Improvement ideas:

* Instead of refreshing the whole page, update only the values.



(Chunk\_size 1024)





REFRESH\_INTERVAL = 1 second:





Max stable pages = 3





REFRESH\_INTERVAL = 3 seconds:





Max stable pages = 6





REFRESH\_INTERVAL = 5 seconds:





Max stable pages = 10





#### Latency



##### Chunksize = 64: 204ms



* \[HTTP] Sent 9826/9826 bytes in 204ms 
* \[HTTP] Sent 9826/9826 bytes in 205ms
* \[HTTP] Sent 9826/9826 bytes in 204ms
* \[HTTP] Sent 9826/9826 bytes in 206ms
* \[HTTP] Sent 9826/9826 bytes in 204ms
* \[HTTP] Sent 9826/9826 bytes in 203ms
* \[HTTP] Sent 9826/9826 bytes in 204ms
* \[HTTP] Sent 9826/9826 bytes in 203ms
* \[HTTP] Sent 9826/9826 bytes in 205ms
* \[HTTP] Sent 9826/9826 bytes in 207ms



##### Chunksize = 128: 115ms



* \[HTTP] Sent 9826/9826 bytes in 127ms
* \[HTTP] Sent 9826/9826 bytes in 113ms
* \[HTTP] Sent 9826/9826 bytes in 115ms
* \[HTTP] Sent 9826/9826 bytes in 115ms
* \[HTTP] Sent 9826/9826 bytes in 114ms
* \[HTTP] Sent 9826/9826 bytes in 117ms
* \[HTTP] Sent 9826/9826 bytes in 115ms
* \[HTTP] Sent 9826/9826 bytes in 115ms
* \[HTTP] Sent 9826/9826 bytes in 115ms
* \[HTTP] Sent 9826/9826 bytes in 116ms



##### Chunksize = 256: 69ms



* \[HTTP] Sent 9826/9826 bytes in 71ms
* \[HTTP] Sent 9826/9826 bytes in 68ms
* \[HTTP] Sent 9826/9826 bytes in 69ms
* \[HTTP] Sent 9826/9826 bytes in 68ms
* \[HTTP] Sent 9826/9826 bytes in 68ms
* \[HTTP] Sent 9826/9826 bytes in 69ms
* \[HTTP] Sent 9826/9826 bytes in 69ms
* \[HTTP] Sent 9826/9826 bytes in 70ms
* \[HTTP] Sent 9826/9826 bytes in 68ms
* \[HTTP] Sent 9826/9826 bytes in 69ms



##### Chunksize = 512: 45ms



* \[HTTP] Sent 9822/9822 bytes in 51ms
* \[HTTP] Sent 9822/9822 bytes in 44ms
* \[HTTP] Sent 9822/9822 bytes in 44ms
* \[HTTP] Sent 9822/9822 bytes in 44ms
* \[HTTP] Sent 9822/9822 bytes in 44ms
* \[HTTP] Sent 9822/9822 bytes in 47ms
* \[HTTP] Sent 9822/9822 bytes in 44ms
* \[HTTP] Sent 9822/9822 bytes in 45ms
* \[HTTP] Sent 9822/9822 bytes in 45ms
* \[HTTP] Sent 9822/9822 bytes in 45ms



##### Chunksize = 1024: 31ms



* \[HTTP] Sent 9854/9822 bytes in 37ms
* \[HTTP] Sent 9822/9822 bytes in 30ms
* \[HTTP] Sent 9822/9822 bytes in 29ms
* \[HTTP] Sent 9822/9822 bytes in 30ms
* \[HTTP] Sent 9822/9822 bytes in 31ms
* \[HTTP] Sent 9822/9822 bytes in 30ms
* \[HTTP] Sent 9822/9822 bytes in 31ms
* \[HTTP] Sent 9822/9822 bytes in 30ms
* \[HTTP] Sent 9822/9822 bytes in 31ms
* \[HTTP] Sent 9822/9822 bytes in 30ms



##### Chunksize = 2048: 22ms



* \[HTTP] Sent 9822/9822 bytes in 23ms
* \[HTTP] Sent 9822/9822 bytes in 22ms
* \[HTTP] Sent 9822/9822 bytes in 22ms
* \[HTTP] Sent 9822/9822 bytes in 21ms
* \[HTTP] Sent 9822/9822 bytes in 22ms
* \[HTTP] Sent 9822/9822 bytes in 22ms
* \[HTTP] Sent 9822/9822 bytes in 22ms
* \[HTTP] Sent 9822/9822 bytes in 22ms
* \[HTTP] Sent 9822/9822 bytes in 22ms
* \[HTTP] Sent 9822/9822 bytes in 22ms







