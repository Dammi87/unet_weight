from __future__ import absolute_import

import argparse
import logging
import re
import os
from unet.common import listdir
from unet.label.convert import mask_to_weight

import apache_beam as beam
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions

def mask_to_weight_spark(input_image):
    return mask_to_weight(input_image, "/home/adamf/data/Karolinska/hmm", 10, 5)


class WeightGenWrap(beam.DoFn):
    def __init__(self):
        super(WeightGenWrap, self).__init__()

    def process(self, element):
        # Need to return a list instead of a string
        return [mask_to_weight_spark(element)] 
def run():
    # We use the save_main_session option because one or more DoFn's in this
    # workflow rely on global context (e.g., a module imported at module level).
    BUCKET = 'gs://datasets-simone/'
    PROJECT = 'karolinska-188312'
    INPUT_LABEL_FOLDER = os.path.join(BUCKET, 'labels')
    OUTPUT_FILE = os.path.join(BUCKET, 'labels.txt')
    pipeline_options = PipelineOptions()
    pipeline_options.view_as(StandardOptions).runner = 'DataflowRunner'
    pipeline_options.view_as(SetupOptions).save_main_session = True
    pipeline_options.view_as(SetupOptions).setup_file = os.path.abspath('../../setup.py')
    google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
    google_cloud_options.project = PROJECT
    google_cloud_options.job_name = "some-adam-jerb7"
    google_cloud_options.staging_location = os.path.join(BUCKET, "staging")
    google_cloud_options.temp_location = os.path.join(BUCKET, "temp")
    p = beam.Pipeline(options=pipeline_options)

    # Create a collection from all the files
    files = (p | beam.Create(listdir(INPUT_LABEL_FOLDER)))
    file_names = (
        files
        | 'weight' >> (beam.ParDo(WeightGenWrap())
                       .with_output_types(unicode))
        | 'names' >> beam.Map(lambda element: os.path.basename(element)))

    file_names | 'write' >> WriteToText(OUTPUT_FILE)

    result = p.run()
    result.wait_until_finish()


if __name__ == "__main__":
    run()
