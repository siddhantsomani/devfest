import argparse

from google.cloud import videointelligence

video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.enums.Feature.LABEL_DETECTION]
operation = video_client.annotate_video('gs://devfest-devfest/MI6.mp4', features=features)
print('\nProcessing video for label annotations:')

result = operation.result(timeout=90)
print('\nFinished processing.')

# first result is retrieved because a single video was processed
segment_labels = result.annotation_results[0].segment_label_annotations
max = 0.0
entity = ''
max1 = 0.0
entity1 = ''
for i, segment_label in enumerate(segment_labels):
    print('Video label description: {}'.format(
        segment_label.entity.description))
    for category_entity in segment_label.category_entities:
        print('\tLabel category description: {}'.format(
            category_entity.description))

    for i, segment in enumerate(segment_label.segments):
        start_time = (segment.segment.start_time_offset.seconds +
                        segment.segment.start_time_offset.nanos / 1e9)
        end_time = (segment.segment.end_time_offset.seconds +
                    segment.segment.end_time_offset.nanos / 1e9)
        positions = '{}s to {}s'.format(start_time, end_time)
        confidence = segment.confidence
        # print('\tSegment {}: {}'.format(i, positions))
        if confidence>max:
            max = confidence
            entity = segment_label.entity.description
        if confidence<max and confidence>max1:
            max1 = confidence
            entity1 = segment_label.entity.description
    #     print('\tConfidence: {}'.format(confidence))
    # print('\n')
print('We find that this is a '+entity+'. We also find that this a '+entity1+'.')

def analyze_shots(path):
    """ Detects camera shot changes. """
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.SHOT_CHANGE_DETECTION]
    operation = video_client.annotate_video(path, features=features)
    print('\nProcessing video for shot change annotations:')

    result = operation.result(timeout=90)
    print('\nFinished processing.')

    # first result is retrieved because a single video was processed
    for i, shot in enumerate(result.annotation_results[0].shot_annotations):
        start_time = (shot.start_time_offset.seconds +
                      shot.start_time_offset.nanos / 1e9)
        end_time = (shot.end_time_offset.seconds +
                    shot.end_time_offset.nanos / 1e9)
        print('\tShot {}: {} to {}'.format(i, start_time, end_time))

analyze_shots('gs://devfest-devfest/MI6.mp4')
