import voice_feature_extraction

parent_dir = 'voices'
tr_sub_dirs = ['training']
ts_sub_dirs = ['test']
tr_features, tr_labels = parse_audio_files(parent_dir,tr_sub_dirs)
ts_features, ts_labels = parse_audio_files(parent_dir,ts_sub_dirs)

tr_labels = one_hot_encode(tr_labels)
ts_labels = one_hot_encode(ts_labels)
