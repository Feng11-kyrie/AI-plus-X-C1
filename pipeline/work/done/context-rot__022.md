### Google

- Gemini 2.5 Pro
- Gemini 2.5 Flash
- Gemini 2.0 Flash

### Alibaba

- Qwen3-235B-A22B
- Qwen3-32B
- Qwen3-8B

## 使用的嵌入模型

- text-embedding-3-small
- text-embedding-3-large
- jina-embeddings-v3（input_type='text-matching'）
- voyage-3-large（input_type=None）
- all-MiniLM-L6-v2

## 针—问题相似度

注：同一模型的思考／非思考模式分开统计

*针—问题相似度 —— arXiv 草堆／PG 文章针*

*针—问题相似度 —— PG 文章草堆／PG 文章针*

*针—问题相似度 —— PG 文章草堆／arXiv 针*

正如我们在针—草堆相似度结果中提到的，我们注意到这一处例外：模型在该组合上的表现相对其它针—草堆组合格外好。单看这一处，可能会以为高性能模型的表现是一致的。然而这种一致性对其余实验并不成立。
