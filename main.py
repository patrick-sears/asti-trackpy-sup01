#!/usr/bin/python3


import sys
import math
import statistics


# if len(sys.argv) < 2:
#   print( "Need config file as argument." )
#   exit( 1 )
# fname_config = sys.argv[1]

n_arg = len(sys.argv)

new_app_files = 0

i = 1
while i < n_arg:
  if sys.argv[i] == '--config':
    i += 1
    fname_config = sys.argv[i]
  elif sys.argv[i] == '--new_app_files':
    i += 1
    new_app_files = int(sys.argv[i])
  else:
    print("Error:  Unrecognized argument.")
    print("  i:        "+str(i))
    print("  argv[i]:  "+sys.argv[i])
    exit(1)
  #
  i += 1



f_config = open( fname_config, 'r' )


############################################ **config
for l in f_config:
  if not l.startswith('!'):  continue
  l = l.strip()
  ll = l.split(' ')
  key = ll[0]
  if key == '!imdir':
    if len(ll) == 2:    imdir = ll[1]
    else:               imdir = f_config.readline().strip()
  elif key == '!um_per_pix':
    um_per_pix = float(ll[1])
  elif key == '!ms_per_frame':
    ms_per_frame = float(ll[1])
  elif key == '!fname_out1':
    fname_out1 = ll[1]
  elif key == '!fname_out2':
    fname_out2 = ll[1]
  elif key == '!track_ims_dir':
    track_ims_dir = ll[1]
  elif key == '!track_ims_vidname':
    track_ims_vidname = ll[1]
  #
  elif key == '!imfile_basename':
    imfile_basename = ll[1]
  elif key == '!imfile_suffix':
    imfile_suffix = ll[1]
  elif key == '!imfile_i_first':
    imfile_i_first = int(ll[1])
  elif key == '!imfile_i_last':
    imfile_i_last = int(ll[1])
  elif key == '!imfile_digs':
    imfile_digs = int(ll[1])
  #
  elif key == '!im_w':
    im_w = int(ll[1])
  elif key == '!im_h':
    im_h = int(ll[1])
  #
  elif key == '!min_frames_in_a_track':
    min_frames_in_a_track = int(ll[1])
  #
  elif key == '!particle_size':
    particle_size = float(ll[1])
  elif key == '!search_range':
    search_range = float(ll[1])
  elif key == '!tpl_minmass':
    tpl_minmass = int(ll[1])
  elif key == '!min_track_len_px':
    min_track_len_px = float(ll[1])
  #
  #
  elif key == '!sup01_f2name':
    sup01_f2name = ll[1]
  elif key == '!sup01_f3name':
    sup01_f3name = ll[1]
  elif key == '!sup01_f4name':
    sup01_f4name = ll[1]
  #
  #
  else:
    print("Unrecognized key.")
    print("  key = ", key)
############################################ **config






############################################

n1 = []
id1 = []
t1 = []
x1 = []
y1 = []

# n1.   int    Number of points in track.
# id1.  int    Original track id from trackpy run.
# t1.   int    Frame #.
# x1.   float  x pos
# y1.   float  y pos


############################################
f1 = open(fname_out1)

l = f1.readline().strip()
ll = l.split(' ')
n_track = int( ll[1] )

l = f1.readline().strip()
ll = l.split(' ')

for i in range(n_track):
  t1.append([])
  x1.append([])
  y1.append([])
  n1.append( int(ll[i+1]) )
  id1.append( -1 )  # unset
  for j in range(n1[i]):
    t1[i].append( 0.0 )
    x1[i].append( 0.0 )
    y1[i].append( 0.0 )




#################################
# i is the track
i = 0
for l in f1:
  if l.startswith('!'):
    # Here, l has form "! track #"
    ll = f1.readline().strip().split(' ')
    if int(ll[1]) != n1[i]:
      print("Error.  Bad n1.")
      exit(1)
    ll = f1.readline().strip().split(' ')
    id1[i] = int(ll[1])
    #
    for l in f1:
      if l == "i_frame x y\n":  break
    j = 0
    for l in f1:
      l = l.strip()
      if len(l) == 0:  break
      if l.startswith('#'):  continue
      ll = l.split('\t')
      t1[i][j] = int(ll[0])
      x1[i][j] = float(ll[1])
      y1[i][j] = float(ll[2])
      j += 1
    if j != n1[i]:
      print("Error.  Didn't read all data.")
      exit(1)
    #
    i += 1
#################################





if i != n_track:
  print("Error.  i != n_track.")
  print("  n_track = ", n_track)
  print("  i       = ", i)
  exit(1)








#######################################################
speed = []
time_len = []
dist_len = []


for i in range( n_track ):
  speed.append( -1.0 )
  time_len.append( -1.0 )
  dist_len.append( -1.0 )




for i in range( n_track ):
  n = n1[i]
  #
  dx = (x1[i][n-1] - x1[i][0]) * um_per_pix
  dy = (y1[i][n-1] - y1[i][0]) * um_per_pix
  # dx, dy in um
  #
  dt = (n-1) * ms_per_frame / 1000.0
  # dt in s
  #
  #
  time_len[i] = dt
  dist_len[i] = math.hypot(dx,dy)
  #
  #
  if dt == 0.0:
    dx = float('nan')
    dy = float('nan')
  else:
    dx /= dt
    dy /= dt
  # dx, dy in um/s.
  #
  speed[i] = math.hypot(dx, dy)
  # math.hypot(float('nan'),float('nan')) returns 'nan'.



mean_time_len = statistics.mean( time_len )
mean_dist_len = statistics.mean( dist_len )
mean_speed = statistics.mean( speed )






#######################################################
f2 = open(sup01_f2name, 'w')

line = "i track_id time_len(s) dist_len(μm) speed(μm/s)"
f2.write(line+'\n')

for i in range(n_track):
  line = str(i)
  line += ' {0:0d}'.format(id1[i])
  line += ' {0:0.6f}'.format(time_len[i])
  line += ' {0:0.6f}'.format(dist_len[i])
  line += ' {0:0.6f}'.format(speed[i])
  f2.write(line+'\n')

# Note the accuracy.
# Time:
#    '.6f' s: 1 us precision
#    120 fr/s -> 8.333 ms = 8333 us.
# Distance:
#    '.6f' um: 1 pm precision

f2.write('\n')
f2.write('mean_time_len(s): {0:0.6f}\n'.format(mean_time_len))
f2.write('mean_dist_len(um): {0:0.6f}\n'.format(mean_dist_len))
f2.write('mean_speed(um/s): {0:0.6f}\n'.format(mean_speed))
f2.write('\n')
f2.write('\n')



line1 = "i    track_id  time_len(s)   dist_len(μm)  speed(μm/s)"
line2 = "---  --------  ------------  ------------  ------------"
#        012  01234567  012345678901  012345678901  012345678901
line3 = "-------------------------------------------------------"

f2.write('\n\n')
f2.write(line3+'\n')
f2.write(line1+'\n')
f2.write(line2+'\n')


for i in range(n_track):
  line = '{0:3d}'.format(i)
  line += '  {0:8d}'.format(id1[i])
  line += '  {0:12.6f}'.format(time_len[i])
  line += '  {0:12.6f}'.format(dist_len[i])
  line += '  {0:12.6f}'.format(speed[i])
  f2.write(line+'\n')


f2.write(line3+'\n')
f2.write('\n')




f34_mode = 'a'
if new_app_files == 1:
  f34_mode = 'w'



#######################################################
# For summary file of many vids - easy to parse

f3 = open(sup01_f3name, f34_mode)
if f34_mode == 'w':
  line = 'vid speed(um/s)'
  f3.write(line+'\n')

line = track_ims_vidname
line += ' {0:0.6f}'.format(mean_speed)
f3.write(line+'\n')



#######################################################
# For summary file of many vids - easy to read
f4 = open(sup01_f4name, f34_mode)
if f34_mode == 'w':
  line = 'vid     speed(um/s)'
  f4.write(line+'\n')

line = track_ims_vidname
line += '  {0:12.6f}'.format(mean_speed)
f4.write(line+'\n')









