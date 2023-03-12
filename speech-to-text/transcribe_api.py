from config import aws_config as config
import boto3
import time
import urllib
import json
import pandas as pd
import datetime

def check_job_name(job_name):
    job_verification = True
    replace_job_loop = True
    # all the transcriptions
    existed_jobs = transcribe.list_transcription_jobs()

    for job in existed_jobs['TranscriptionJobSummaries']:
        if job_name == job['TranscriptionJobName']:
            job_verification = False
            break
    if job_verification == False:
        while(replace_job_loop):
            command = input(job_name + " has existed. \nDo you want to override the existed job (Y/N): ")
            if command.lower() == "y" or command.lower() == "yes":
                transcribe.delete_transcription_job(TranscriptionJobName=job_name)
                replace_job_loop = False
            elif command.lower() == "n" or command.lower() == "no":
                job_name = input("Insert new job name? ")
                check_job_name(job_name)
                replace_job_loop = False
            else: 
                print("Input can only be (Y/N)")

    return job_name


def amazon_transcribe_single_speaker(bucket_link, audio_file_name):
  job_uri = bucket_link + audio_file_name 
  # 
  # Usually, I put like this to automate the process with the file name
  # "s3://bucket_name" + audio_file_name 

  # Usually, file names have spaces and have the file extension like .mp3
  # we take only a file name and delete all the space to name the job
  job_name = (audio_file_name.split('.')[0]).replace(" ", "")
  
  # file format
  file_format = audio_file_name.split('.')[1]

  # check if name is taken or not
  job_name = check_job_name(job_name)
  transcribe.start_transcription_job(
      TranscriptionJobName=job_name,
      Media={'MediaFileUri': job_uri},
      MediaFormat = file_format,
      LanguageCode='en-US')
  
  while True:
    result = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if result['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
      print("FAILED")
      break
    time.sleep(15)

  if result['TranscriptionJob']['TranscriptionJobStatus'] == "COMPLETED":
    data = pd.read_json(result['TranscriptionJob']['Transcript']['TranscriptFileUri'])
  
  return data['results'][1][0]['transcript']



def amazon_transcribe_multiple_speakers(bucket_link,audio_file_name, max_speakers = -1):

  if max_speakers > 10:
    raise ValueError("Maximum detected speakers is 10.")

  job_uri = "s3 bucket link" + audio_file_name 
  job_name = (audio_file_name.split('.')[0]).replace(" ", "")
  
  # check if name is taken or not
  job_name = check_job_name(job_name)
  
  if max_speakers != -1:
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat=audio_file_name.split('.')[1],
        LanguageCode='en-US',
        Settings = {'ShowSpeakerLabels': True,
                  'MaxSpeakerLabels': max_speakers
                  }
    )
  else: 
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat=audio_file_name.split('.')[1],
        LanguageCode='en-US',
        Settings = {'ShowSpeakerLabels': True
                  }
    )    
  
  while True:
    result = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if result['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    time.sleep(15)
  if result['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
    data = pd.read_json(result['TranscriptionJob']['Transcript']['TranscriptFileUri'])
  return result


def read_output(filename):
  # example filename: audio.json
  
  # take the input as the filename
  
  filename = (filename).split('.')[0]

  # Create an output txt file
  print(filename+'.txt')
  with open(filename+'.txt','w') as w:
    with open(filename+'.json') as f:

      data=json.loads(f.read())
      labels = data['results']['speaker_labels']['segments']
      speaker_start_times={}
      
      for label in labels:
        for item in label['items']:
          speaker_start_times[item['start_time']] = item['speaker_label']

      items = data['results']['items']
      lines = []
      line = ''
      time = 0
      speaker = 'null'
      i = 0

      # loop through all elements
      for item in items:
        i = i+1
        content = item['alternatives'][0]['content']

        # if it's starting time
        if item.get('start_time'):
          current_speaker = speaker_start_times[item['start_time']]
        
        # in AWS output, there are types as punctuation
        elif item['type'] == 'punctuation':
          line = line + content

        # handle different speaker
        if current_speaker != speaker:
          if speaker:
            lines.append({'speaker':speaker, 'line':line, 'time':time})
          line = content
          speaker = current_speaker
          time = item['start_time']
          
        elif item['type'] != 'punctuation':
          line = line + ' ' + content
      lines.append({'speaker': speaker, 'line': line,'time': time})

      # sort the results by the time
      sorted_lines = sorted(lines,key=lambda k: float(k['time']))

      # write into the .txt file
      for line_data in sorted_lines:
        line = '[' + str(datetime.timedelta(seconds=int(round(float(line_data['time']))))) + '] ' + line_data.get('speaker') + ': ' + line_data.get('line')
        w.write(line + '\n\n')




transcribe = boto3.client('transcribe',
                          aws_access_key_id = config.ACCESS_KEY,
                          aws_secret_access_key = config.SECRET_KEY,
                          region_name = config.REGION,
)
bucket_link = r's3://content-pwd-aat/transcribe-content/'
audio_file_name_s3 = "1. Step 01 - Exploring Lazy and Eager Initialization of Spring Framework Beans.mp4"

#single speaker transcribtion
transcript_file = amazon_transcribe_single_speaker(bucket_link,audio_file_name_s3)

#multiple speaker transcribtion
# amazon_transcribe_multiple_speakers(bucket_link,audio_file_name_s3)

# define AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and bucket_name
# bucket_name: name of s3 storage folder
s3 = boto3.client('s3', 
  aws_access_key_id = config.ACCESS_KEY,
  aws_secret_access_key = config.SECRET_KEY,
  region_name = config.REGION)
  
# save transcribed file to s3 bucket
s3.upload_file(transcript_file, "content-pwd-aat/transcribe-content", (audio_file_name_s3 + "_transcript"))