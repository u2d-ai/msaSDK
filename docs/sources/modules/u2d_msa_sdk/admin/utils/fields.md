#


### Field
```python
.Field(
   default: Any = Undefined, *, default_factory: Optional[NoArgAnyCallable] = None,
   alias: str = None, title: str = None, description: str = None,
   exclude: Union[AbstractSet[Union[int, str]], Mapping[Union[int, str], Any],
   Any] = None, include: Union[AbstractSet[Union[int, str]], Mapping[Union[int,
   str], Any], Any] = None, const: bool = None, gt: float = None, ge: float = None,
   lt: float = None, le: float = None, multiple_of: float = None, min_items: int = None,
   max_items: int = None, min_length: int = None, max_length: int = None,
   allow_mutation: bool = True, regex: str = None, primary_key: bool = False,
   foreign_key: Optional[Any] = None, unique: bool = False, nullable: Union[bool,
   UndefinedType] = Undefined, index: Union[bool, UndefinedType] = Undefined,
   sa_column: Union[Column, UndefinedType] = Undefined,
   sa_column_args: Union[Sequence[Any], UndefinedType] = Undefined,
   sa_column_kwargs: Union[Mapping[str, Any], UndefinedType] = Undefined,
   schema_extra: Optional[Dict[str, Any]] = None, msa_ui_form_item: Union[FormItem,
   dict, str] = None, msa_ui_filter_item: Union[FormItem, dict, str] = None,
   msa_ui_table_column: Union[TableColumn, dict, str] = None
)
```

