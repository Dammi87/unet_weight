import os

cmd = "python -m unet.dataproc.submit_job_to_cluster"
cmd = "%s \\\n\t%s" % (cmd, "--project_id %s" % "karolinska-188312")
cmd = "%s \\\n\t%s" % (cmd, "--zone %s" % "europe-west1-b")
cmd = "%s \\\n\t%s" % (cmd, "--cluster_name %s" % "leshit7")
cmd = "%s \\\n\t%s" % (cmd, "--gcs_bucket %s" % "datasets-simone")
cmd = "%s \\\n\t%s" % (cmd, "--pyspark_file %s" % os.path.abspath("../label/pyspark/run.py"))
cmd = "%s \\\n\t%s" % (cmd, "--create_new_cluster")
print(cmd)
os.system(cmd)