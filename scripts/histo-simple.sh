csvcut -c course_over_ground kine-filterd.csv | grep -v ground | awk '{print  int(($1)/45)*45}' | sort | uniq -c 
csvcut -c speed_over_ground kine-filterd.csv | grep -v ground | sort | uniq  -c


https://github.com/gdamjan/uv-getting-started