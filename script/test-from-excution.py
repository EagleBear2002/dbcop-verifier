import subprocess
import os
import shutil

def reset_dir(dir):
  if not os.path.exists(dir):
    os.mkdir(dir)
  if len(os.listdir(dir)) != 0:
    print(f'{dir} is not empty, clear it')
    shutil.rmtree(dir)

root_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
dbcop_path = os.path.join(root_path, 'target', 'release', 'dbcop')

# history_dir_name = 'roachdb_general_all_writes' 
history_dir_name = 'roachdb_general_partition_writes' 
history_dir = os.path.join(root_path, 'excutions', history_dir_name)

output_dir = os.path.join(root_path, 'results', history_dir_name)
reset_dir(output_dir)

for hist in os.listdir(history_dir):
  hist_out_dir = os.path.join(output_dir, hist)
  reset_dir(hist_out_dir)
  for spec_hist in os.listdir(os.path.join(history_dir, hist)):
    out_dir = os.path.join(hist_out_dir, spec_hist)
    reset_dir(out_dir)
    print(out_dir)

    ver_dir = os.path.join(history_dir, hist, spec_hist)
    cmd = [dbcop_path, 'verify', 
                       '-c', 'ser',
                       '--out_dir', out_dir,
                       '--ver_dir', ver_dir]
    
    subprocess.run(cmd, stdout=subprocess.DEVNULL)

