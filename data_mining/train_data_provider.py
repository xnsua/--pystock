import numpy as np

from data_mining import data_preprocess
from stock_data_manager.ddr_file_cache import read_ddr_fast


def _combine_train_datas(train_datas):
    zip_value = list(zip(*train_datas))
    datas = [val for item in zip_value[0] for val in item]
    labels = [val for item in zip_value[1] for val in item]
    return datas, labels


class TrainDataProvider:
    @staticmethod
    def provide_single(code, feature_extractors, label_extractors):
        ddr = read_ddr_fast(code)
        df = ddr.df
        df = data_preprocess.MissingValue.fill_with_previous(df)
        all_features = []
        # extract feature
        for extractor in feature_extractors:
            features = extractor(df)
            if isinstance(features, tuple) or isinstance(features, list):
                all_features.extend(features)
            elif isinstance(features, np.ndarray):
                all_features.append(features)
            else:
                assert False, f'Unknown features {features}'

        # Skip items that may do not have feature
        skip_items = 50
        # remove invalid value
        for i, feature in enumerate(all_features):
            all_features[i] = feature[skip_items - 1:-1]

        label = label_extractors(df)
        label = label[skip_items:]

        feature2 = np.asarray(all_features).T

        # scaler = StandardScaler()
        # scaler.fit(feature2)
        # feature2 = scaler.transform(feature2)
        date_index =df.index.values[skip_items:]
        return date_index, (feature2, label)
