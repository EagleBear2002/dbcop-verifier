import subprocess
import os
import shutil

def reset_dir(dir):
  if not os.path.exists(dir):
    os.makedirs(dir)
  if len(os.listdir(dir)) != 0:
    print(f'{dir} is not empty, clear it')
    shutil.rmtree(dir)

project_path = os.path.join('.')
dbcop_path = os.path.join(project_path, 'target', 'release', 'dbcop')
excutions_dir_names = [
  # 'antidote_all_writes',
  'galera_all_writes',
  # 'galera_partition_writes',
  # 'roachdb_all_writes',
  # 'roachdb_general_all_writes',
  # 'roachdb_general_partition_writes',
  # 'roachdb_partition_writes',
  # 'diy_excutions',
]

def verify_history_dir(excutions_dir_name):
  excutions_dir = os.path.join(project_path, 'excutions', excutions_dir_name) # eg. antidote_all_writes

  output_dir = os.path.join(project_path, 'results', 'results-status-cnt-improved-building-graph', excutions_dir_name)
  reset_dir(output_dir)

  for hist in os.listdir(excutions_dir): # eg. 3_30_20_180
    hist_out_dir = os.path.join(output_dir, hist)
    reset_dir(hist_out_dir)
    for spec_hist in os.listdir(os.path.join(excutions_dir, hist)): # eg. hist-00000
      out_dir = os.path.join(hist_out_dir, spec_hist)
      reset_dir(out_dir)
      print(out_dir)

      ver_dir = os.path.join(excutions_dir, hist, spec_hist)
      cmd = [dbcop_path, 'verify',
                         '-c', 'ser',
                         '--out_dir', out_dir,
                         '--ver_dir', ver_dir]

      subprocess.run(cmd, stdout=subprocess.DEVNULL)

for excutions_dir_name in excutions_dir_names:
  verify_history_dir(excutions_dir_name)