We make this class "Abstract" by importing **ABC** from the **abc** library

```python
from abc import ABC, abstractmethod
```

We inherit from `ABC` to create this Class as Abstract.

```python
class Shape(ABC):
```

We use the `@abstractmethod` **decorator** to specify we need to implement this method in the child class.

```python    
    @abstractmethod
    def getArea(self):
        raise NotImplementedError
```