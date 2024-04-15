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
history_dir_names = [
  # 'antidote_all_writes',
  # 'galera_all_writes',
  # 'galera_partition_writes',
  # 'roachdb_all_writes',
  'roachdb_general_all_writes',
  'roachdb_general_partition_writes',
  'roachdb_partition_writes'
]

def verify_history_dir(history_dir_name):
  history_dir = os.path.join(project_path, 'excutions', history_dir_name)

  output_dir = os.path.join(project_path, 'results-status-cnt', history_dir_name)
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

for history_dir_name in history_dir_names:
  verify_history_dir(history_dir_name)