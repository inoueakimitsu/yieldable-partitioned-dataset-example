# Yieldable Partitioned Dataset Example

## Overview
A custom dataset for handling PartitionedDataSets that contain too many files to be loaded into memory.

It differs from the original `PartitionedDataSet` in that a generator can be given at save time instead of a dict.
Each time you yield, one file will be written. This method makes it possible to output the data set sequentially without storing it in memory.

The generator should be designed to yield a tuple of keys and values. An example is shown below.

```yaml:conf/base/catalog.yml
example_dataset:
  type: yieldable_partitioned_dataset_example.extras.datasets.yieldable_dataset.YieldablePartitionedDataSet
  path: data/01_raw/example_dataset
  dataset: pandas.CSVDataSet
```

```python
def create_example_partitioned_dataset():

    for i in range(5):

        # please yield a tuple of key and value
        yield f"{i % 2}/{i}.csv", pd.DataFrame({"x":np.arange(10), "y":np.array([i for _ in range(10)])})
```
There is an implementation of a custom dataset in `src/yieldable_partitioned_dataset_example/extras/datasets/yiedable_dataset.py`
