import json
import yaml
import os
import pprint
import re
import pickle

syaml = yaml.load(open('./audit-sources.yaml').read(),Loader=yaml.FullLoader)
versions={}

# for bucket, entry in syaml['buckets'].items():
#     #only grab the first bucket
#     job = entry['jobs'][0] 
#     tests = yaml.load(
#         open(os.path.join('./data-gen/processed',
#                           bucket,job,'tests.json')
#         ).read(),Loader=yaml.FullLoader)
#     metadata = yaml.load(
#         open(os.path.join('./data-gen/processed',
#                           bucket,job,'metadata.json')
#         ).read(),Loader=yaml.FullLoader)
#     version = metadata['revision'].split('+')[0].split('-')[0]
#     versions[version] = tests

# jar = open('versions.pickle','w')
# pickle.dump(versions,jar)
# jar.close()
pickle_jar = open('versions.pickle','r')
versions = pickle.load(pickle_jar)
pickle_jar.close()
# import ipdb; ipdb.set_trace(context=60)

tagless_tests={}
for version, tests in versions.items():
    for test_name, test_entry in tests.items():
        tags = re.findall(r'\[.+?\]', test_name)
        tagless_name = test_name
        for tag in tags:
            tagless_name = tagless_name.replace(tag,'').strip()
        if not tagless_tests.has_key(tagless_name):
            tagless_tests[tagless_name] = {"test_names":{},"test_tags":{}}
        tagless_tests[tagless_name]["test_names"][version]=test_name
        tagless_tests[tagless_name]["test_tags"][version]=tags
        tagless_tests[tagless_name]["removed_tags"]={}
        tagless_tests[tagless_name]["added_tags"]={}
        tagless_tests[tagless_name]["added_test"]={}
        tagless_tests[tagless_name]["removed_test"]={}

version_list=sorted(versions.keys())
for tagless_name, data in tagless_tests.items():
    for version_idx in range(len(version_list[1:])):
        current_version=version_list[version_idx+1]
        # skip to next version if this version doesn't have any tests
        if not data['test_names'].has_key(current_version):
            continue
        previous_version=version_list[version_idx]
        # If there is a previous and current version this isn't a new test
        if data['test_names'].has_key(previous_version) and \
           data['test_names'].has_key(current_version):
            previous_test_name = data['test_names'][previous_version]
            previous_test_tags = data['test_tags'][previous_version]
            current_test_tags = data['test_tags'][current_version]
            removed_tags = sorted(list(set(sorted(previous_test_tags)) - set(current_test_tags)))
            added_tags = sorted(list(set(sorted(current_test_tags)) - set(previous_test_tags)))
            if removed_tags:
                tagless_tests[tagless_name]["removed_tags"][current_version]=removed_tags
            if added_tags:
                tagless_tests[tagless_name]["added_tags"][current_version]=added_tags
        # If there is a previous version and not a current version we deleted it
        elif data['test_names'].has_key(previous_version) and not data['test_names'].has_key(current_version):
            tagless_tests[tagless_name]["deleted_test"][current_version]=True
        # Else this IS a now test, with fresh tags
        else:
            tagless_tests[tagless_name]["added_test"][current_version]=True
        previous_version = current_version

# import ipdb; ipdb.set_trace(context=60)
version_summary={}
test_summary={}
for tagless_name, data in tagless_tests.items():
    test_versions = sorted(data['test_names'].keys())
    final_test_name=data['test_names'][test_versions[-1]]
    for version_idx in range(len(test_versions)):
        current_version=test_versions[version_idx]
        if data['removed_tags'].has_key(current_version) or \
           data['added_tags'].has_key(current_version) or \
           data['added_test'].has_key(current_version):
            # create the hashes for this version
            if not version_summary.has_key(current_version):
                version_summary[current_version]={}
            version_summary[current_version][final_test_name]={}
            # create the hashes for this final_test_name
            if not test_summary.has_key(final_test_name):
                test_summary[final_test_name]={}
            test_summary[final_test_name][current_version]={}
        if data['removed_tags'].has_key(current_version):
            test_summary[final_test_name][current_version]['removed_tags']\
                =data['removed_tags'][current_version]
            version_summary[current_version][final_test_name]['removed_tags']\
                =data['removed_tags'][current_version]
        if data['added_tags'].has_key(current_version):
            test_summary[final_test_name][current_version]['added_tags']\
                =data['added_tags'][current_version]
            version_summary[current_version][final_test_name]['added_tags']\
                =data['added_tags'][current_version]
        if data['added_test'].has_key(current_version):
            test_summary[final_test_name][current_version]['added_test']\
                =data['added_test'][current_version]
            version_summary[current_version][final_test_name]['added_test']\
                =data['added_test'][current_version]
        print current_version
    pass

