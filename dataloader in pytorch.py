import numpy as np
import collections
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torch.utils.data.sampler import BatchSampler, Sampler, SequentialSampler

def Stack(arrays):
    new_dim_array = [np.expand_dims(array, axis=0) for array in arrays]
    return np.concatenate(new_dim_array, axis=0)
    
def my_collect(batch):
    "Puts each data field into a tensor with outer dimension batch size"
    if isinstance(batch[0], (np.ndarray, np.generic)):
        return Stack(batch)
    elif isinstance(batch[0], int):
        return np.array(batch, dtype=np.int)
    elif isinstance(batch[0], float):
        return np.array(batch, dtype=np.float)
    elif isinstance(batch[0], (str, bytes)):
        return batch
    elif isinstance(batch[0], collections.Mapping):
        return {key: my_collect([d[key] for d in batch]) for key in batch[0]}
    elif isinstance(batch[0], collections.Sequence):
        transposed = zip(*batch)
        return [my_collect(samples) for samples in transposed]
    
    error_msg = "batch must contain tensors, numbers, dicts or lists; found {}"
    raise TypeError((error_msg.format(type(batch[0]))))
    
class MyData(Dataset):
    def __init__(self):
        self.lst = list(range(100, 115))
        
    def __getitem__(self, index):
        return self.lst[index]

    def __len__(self):
        return len(self.lst)
     
def PrintLoader(loader):
    for b in loader:
        print(b)
        
def TestShuffle():
    myset = MyData()
    loader_a = DataLoader(myset, batch_size=4, shuffle=False)
    loader_b = DataLoader(myset, batch_size=4, shuffle=True)
    print('using shuffle=False:')
    PrintLoader(loader_a)
    print('using shuffle=True:')
    PrintLoader(loader_b)
        
def TestMyCollect():
    myset = MyData()
    loader_a = DataLoader(myset, batch_size=4, collate_fn=my_collect, shuffle=False)
    loader_b = DataLoader(myset, batch_size=4, shuffle=False)
    print('merge batch into tensor:')
    PrintLoader(loader_a)
    print('merge batch into numpy array:')
    PrintLoader(loader_b)
    
def TestBatch():
    myset = MyData()
    sampler = SequentialSampler(myset)
    batch_sampler = BatchSampler(sampler, batch_size=4, drop_last=False)
    loader_a = DataLoader(myset, batch_size=4, collate_fn=my_collect, shuffle=False)
    loader_b = DataLoader(myset, batch_sampler=batch_sampler, collate_fn=my_collect, shuffle=False)
    print('data for using default sampler:')
    PrintLoader(loader_a)
    print('data for using user defined sampler:')
    PrintLoader(loader_b)   

class RepeatSampler(Sampler):
    def __init__(self, sampler, repeat=5):
        self.sampler = sampler
        self.repeat = repeat

    def __iter__(self):
        for idx in self.sampler:
            batch = []
            for _ in range(self.repeat):
                batch.append(idx)
            yield batch
            
    def __len__(self):
        return len(self.sampler)
       
def TestRepeatSampler():
    myset = MyData()
    sampler = SequentialSampler(myset)
    batch_sampler = RepeatSampler(sampler)
    loader = DataLoader(myset, batch_sampler=batch_sampler, collate_fn=my_collect, shuffle=False)
    print('data for using repeat sampler:')
    PrintLoader(loader)
    
if __name__=='__main__':
    #TestShuffle()
    #TestMyCollect()
    #TestBatch()
    TestRepeatSampler()