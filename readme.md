# draw_fasttq
Count the mass scores in fasttq files and draw statistical graphs
# Quickstart
## Dependencies#
+ python3
+ sample fastq files
## Build
in root dir
```
python -r ./requirements.txt
python main.py
```
## conf.yml
+ fastq_file: The name of the file to read
+ result: Generated file suffix
+ read_line: The interval to be read, the two-dimensional array, each element [0], the element [1] represents the start and end of the read, and the left closes the right open interval.
+ title_name: Title name
+ x_name: Abscissa name
+ y_name: Ordinate name
+ ddof: True means sample variance, sample standard deviation, false means population variance, population standard deviation 

# result
## 0-100
![0-100-result](result/MGISEQ2000_PCR-free_NA12878_1_V100003043_L01_1.fq/0-100-result.jpg)
## 1000-1100-result
![1000-1100-result](result/MGISEQ2000_PCR-free_NA12878_1_V100003043_L01_1.fq/1000-1100-result.jpg)
## 10000-10100-result
![1000-1100-result](result/MGISEQ2000_PCR-free_NA12878_1_V100003043_L01_1.fq/10000-10100-result.jpg)