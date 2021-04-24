from typing import Dict, Any, Union, Type, Generator, Tuple
from copy import deepcopy
from kedro.io import PartitionedDataSet
from kedro.io.core import AbstractDataSet

class YieldablePartitionedDataSet(PartitionedDataSet):
    def __init__(  # pylint: disable=too-many-arguments
        self,
        path: str,
        dataset: Union[str, Type[AbstractDataSet], Dict[str, Any]],
        filepath_arg: str = "filepath",
        filename_suffix: str = "",
        credentials: Dict[str, Any] = None,
        load_args: Dict[str, Any] = None,
        fs_args: Dict[str, Any] = None,
    ):        
        super().__init__(path, dataset, filepath_arg, filename_suffix, credentials, load_args, fs_args)

    def _save(self, data: Union[Dict[str, Any], Generator[Tuple[str, Any], None, None]]) -> None:
        # you can pass generator instead of conventional dict object
        _data = sorted(data.items()) if type(data) == dict else data

        for partition_id, partition_data in _data:
            kwargs = deepcopy(self._dataset_config)
            partition = self._partition_to_path(partition_id)
            # join the protocol back since tools like PySpark may rely on it
            kwargs[self._filepath_arg] = self._join_protocol(partition)
            dataset = self._dataset_type(**kwargs)  # type: ignore
            dataset.save(partition_data)
        self._invalidate_caches()
