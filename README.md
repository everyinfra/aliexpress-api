# AliExpress API（速卖通 API）

[English](#english) · [中文](#中文)

## English

This repo reads public AliExpress data with Python or curl. You can search products by keyword and read a product's details, variants, reviews and rating summary. You need one EveryInfra API key. You do not need an AliExpress account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 5 capabilities cost $1.39 per 1,000 calls (about $0.0014 per call). Failed calls and empty results are not charged. The EveryInfra AliExpress API has 6 capabilities, all listed on the platform page: <https://everyinfra.com/en/aliexpress-api?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

### Quick start

```bash
git clone https://github.com/everyinfra/aliexpress-api.git
cd aliexpress-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py search "wireless earbuds" --out products.csv
python main.py product "<product url>" --out product.json
python main.py reviews "<product url>" --out reviews.csv
python main.py variants "<product url>" --out variants.csv
python main.py ratings "<product url>" --out ratings.json
```

- For `product`, `reviews`, `variants` and `ratings`, pass a product link such as https://www.aliexpress.com/item/<product id>.html. The `url` from a `search` result works.
- `product` prices for the US and in USD by default.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"aliexpress","action":"search","params":{"keyword":"wireless earbuds"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `product_detail`, `reviews`, `variants`, and `ratings` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `search` | $1.39 |
| `product_detail` | $1.39 |
| `reviews` | $1.39 |
| `variants` | $1.39 |
| `ratings` | $1.39 |

- Billing is per call, about $0.0014 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- `search` is billed by the rows you ask for: every 50 rows count as one call, and blocks that come back with no rows are not charged.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>
- Prices for the 1 other AliExpress capability are on the platform page: <https://everyinfra.com/en/aliexpress-api?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

### Fields

These are the fields that the 5 capabilities returned in our test. Each meaning is the first sentence of the field's entry in the API documentation. The link under each table has the full text.

#### `search` (keyword search)

| Field | Meaning |
|---|---|
| `product_id` | Product ID. |
| `title` | Title. null when the platform has no titles (for example text-only posts). |
| `url` | Link to the record on the platform. |
| `price` | Price as a number without a currency symbol; see currency. |
| `currency` | Currency code of the price (for example CNY, USD). |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). |
| `orders_count` | Total number of orders. |
| `image_url` | Image link. |
| `free_shipping` | Whether shipping is free. |
| `search_rank` | Position in this search result (search). |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `tags` | Array of tags. |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. |

All parameters and fields: <https://everyinfra.com/en/aliexpress-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

#### `product_detail` (product details)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `price` | Price as a number without a currency symbol; see currency. |
| `original_price` | Original price (strikethrough price). |
| `currency` | Currency code of the price (for example CNY, USD). |
| `discount` | Discount level. |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). |
| `review_count` | Number of reviews, for product and business capabilities. null means not disclosed, not 0. |
| `shipping` | Shipping fee and delivery method. |
| `variants` | SKU list, one entry per variant: sku_id, properties (option name → value, such as Color and Size), price, original_price, stock, available, image_url and max_buy_count; keys the platform does not show are left out. |
| `store_name` | Store name. |
| `store_url` | Store link. |
| `image_url` | Image link. |
| `images` | Image links: on product capabilities the product gallery in page order, on reviews the buyer's photos. |
| `description_images` | Images in the product description area. |
| `sold_text` | Sales figure as shown (for example 10,000+ sold); a rounded display, not an exact count. |
| `attributes` | Product attributes as {name, value} rows (material, model and so on). |
| `category_id` | AliExpress category ID. |
| `category_path` | AliExpress category path. |
| `ship_to` | The destination country or region this price and shipping quote applies to. |
| `total_stock` | Total stock across all variants; each variant's own stock is in its variants entry. |
| `video_url` | Product video link. |
| `store_id` | Store ID. |
| `seller_id` | Seller ID (AliExpress's own public ID). |
| `store_country` | Country or region of the store. |
| `store_opened_at` | When the store opened. |
| `store_is_top_rated` | Whether the store is an AliExpress Top Rated seller. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. |

All parameters and fields: <https://everyinfra.com/en/aliexpress-api/product_detail?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

#### `reviews` (reviews)

| Field | Meaning |
|---|---|
| `review_id` | Review ID. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `country` | Country or region: a full name or an ISO code depending on the platform, not normalized. |
| `sku_info` | SKU variant information (combination of color, size and so on). |
| `helpful_count` | Number of times the review was marked helpful. |
| `logistics` | Shipping option. |
| `product_id` | Product ID. |
| `is_anonymous` | Whether the review was posted anonymously (reviews). |
| `unhelpful_count` | How many times the review was marked not helpful (reviews). |
| `language` | Content language code (for example zh, en) as judged by the platform; it can be wrong. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. |

All parameters and fields: <https://everyinfra.com/en/aliexpress-api/reviews?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

#### `variants` (variants)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `price` | Price as a number without a currency symbol; see currency. |
| `original_price` | Original price (strikethrough price). |
| `currency` | Currency code of the price (for example CNY, USD). |
| `discount` | Discount level. |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). |
| `review_count` | Number of reviews, for product and business capabilities. null means not disclosed, not 0. |
| `shipping` | Shipping fee and delivery method. |
| `variants` | SKU list, one entry per variant: sku_id, properties (option name → value, such as Color and Size), price, original_price, stock, available, image_url and max_buy_count; keys the platform does not show are left out. |
| `store_name` | Store name. |
| `store_url` | Store link. |
| `image_url` | Image link. |
| `images` | Image links: on product capabilities the product gallery in page order, on reviews the buyer's photos. |
| `description_images` | Images in the product description area. |
| `sold_text` | Sales figure as shown (for example 10,000+ sold); a rounded display, not an exact count. |
| `attributes` | Product attributes as {name, value} rows (material, model and so on). |
| `category_id` | AliExpress category ID. |
| `category_path` | AliExpress category path. |
| `ship_to` | The destination country or region this price and shipping quote applies to. |
| `total_stock` | Total stock across all variants; each variant's own stock is in its variants entry. |
| `video_url` | Product video link. |
| `store_id` | Store ID. |
| `seller_id` | Seller ID (AliExpress's own public ID). |
| `store_country` | Country or region of the store. |
| `store_opened_at` | When the store opened. |
| `store_is_top_rated` | Whether the store is an AliExpress Top Rated seller. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. |

All parameters and fields: <https://everyinfra.com/en/aliexpress-api/variants?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

#### `ratings` (rating summary)

| Field | Meaning |
|---|---|
| `average_star` | Average star rating. |
| `total_reviews` | Total number of reviews (reviews with written text). |
| `positive_rate` | Positive rating share, as a percentage (94.1 means 94.1%). |
| `negative_rate` | Negative rating share, as a percentage. |
| `five_star` | Five-star ratings, with count (number of ratings, including star-only ratings without text). |
| `four_star` | Four-star ratings, with count. |
| `three_star` | Three-star ratings, with count. |
| `two_star` | Two-star ratings, with count. |
| `one_star` | One-star ratings, with count. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/aliexpress-api/ratings?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

### FAQ

**Do I need an AliExpress account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $1.39 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

**Can I connect the AliExpress API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>.

**What legal points apply when I use AliExpress data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which AliExpress data can I get?**

The EveryInfra AliExpress API has 6 capabilities:

- keyword search
- profile or object details
- variants
- reviews
- rating summary
- product details

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/aliexpress-api?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

### Tested

Before release, we ran the 5 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py search "wireless earbuds" --out products.csv` | 2026-11-25 13:22 | 18 | $0.001389 |
| `python main.py product "<product url>" --out product.json` | 2026-11-25 13:22 | 1 | $0.001389 |
| `python main.py reviews "<product url>" --out reviews.csv` | 2026-11-25 13:23 | 20 | $0.001389 |
| `python main.py variants "<product url>" --out variants.csv` | 2026-11-25 13:27 | 1 | $0.001389 |
| `python main.py ratings "<product url>" --out ratings.json` | 2026-11-25 15:31 | 1 | $0.001389 |

## 中文

本仓库用 Python 或 curl 读速卖通公开数据：按关键词搜商品，读商品详情、规格变体、评价和评分汇总。只需一把 EveryInfra API Key，不用速卖通账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 5 个能力每千次 $1.39（每次约 $0.0014），失败和空结果不收费。速卖通共 6 个能力：<https://everyinfra.com/aliexpress-api?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/aliexpress-api.git
cd aliexpress-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py search "wireless earbuds" --out products.csv
python main.py product "<商品链接>" --out product.json
python main.py reviews "<商品链接>" --out reviews.csv
python main.py variants "<商品链接>" --out variants.csv
python main.py ratings "<商品链接>" --out ratings.json
```

- `product`、`reviews`、`variants`、`ratings` 传商品链接，形如 https://www.aliexpress.com/item/<商品 ID>.html，可用 `search` 结果里的 `url`。
- `product` 默认按美国站、美元查价。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"aliexpress","action":"search","params":{"keyword":"wireless earbuds"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`product_detail`、`reviews`、`variants`、`ratings` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 关键词搜索 | `search` | $1.39 |
| 商品详情 | `product_detail` | $1.39 |
| 评价 | `reviews` | $1.39 |
| 商品变体 | `variants` | $1.39 |
| 评分汇总 | `ratings` | $1.39 |

- 按调用次数计费，每次约 $0.0014；失败、空结果、参数错误和鉴权失败都不收费。
- `search` 按要的条数计费，每 50 条算一次调用，没返回数据的部分不收费。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>
- 速卖通其他 1 个能力的单价见平台页 <https://everyinfra.com/aliexpress-api?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

### 返回字段

下面是这 5 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `search`（关键词搜索）

| 字段 | 含义 |
|---|---|
| `product_id` | 商品 ID。 |
| `title` | 标题。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `price` | 价格数值，不含货币符号；币种见 currency。 |
| `currency` | 价格币种代码（如 CNY、USD）。 |
| `rating` | 评分。 |
| `orders_count` | 累计订单数。 |
| `image_url` | 图片链接。 |
| `free_shipping` | 是否包邮。 |
| `search_rank` | 在本次搜索结果中的位置（search）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `tags` | 标签数组。 |
| `rating_scale` | 上一列 `rating` 的满分。 |

完整参数和字段：<https://everyinfra.com/aliexpress-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

#### `product_detail`（商品详情）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `name` | 名称。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `price` | 价格数值，不含货币符号；币种见 currency。 |
| `original_price` | 原价（划线价）。 |
| `currency` | 价格币种代码（如 CNY、USD）。 |
| `discount` | 折扣力度。 |
| `rating` | 评分。 |
| `review_count` | 评价条数，用于商品/商家类能力。 |
| `shipping` | 运费与配送方式。 |
| `variants` | 规格（SKU）列表，每项一个规格：sku_id、properties（规格名 → 取值，如 Color、Size）、price、original_price、stock、available、image_url、max_buy_count；平台没给的项不出现。 |
| `store_name` | 店铺名称。 |
| `store_url` | 店铺链接。 |
| `image_url` | 图片链接。 |
| `images` | 图片链接：商品类能力里是商品轮播图（按商品页顺序），reviews 里是买家晒图。 |
| `description_images` | 商品描述区图片，来自受限的 AliExpress 媒体正文地址。 |
| `sold_text` | 销量原文（如「10,000+ sold」）；是平台展示的约数，不是精确销量。 |
| `attributes` | 商品属性列表（材质、型号等 {name, value} 行）。 |
| `category_id` | 分类 ID。 |
| `category_path` | 分类路径。 |
| `ship_to` | 这次报价与运费对应的收货国家/地区。 |
| `total_stock` | 商品总库存（各规格合计；单个规格的库存在 variants 每项的 stock）。 |
| `video_url` | 商品视频链接。 |
| `store_id` | 店铺 ID。 |
| `seller_id` | 卖家 ID（速卖通自己的公开 ID）。 |
| `store_country` | 店铺所在国家/地区。 |
| `store_opened_at` | 店铺开设时间。 |
| `store_is_top_rated` | 店铺是否为平台优质卖家（Top Rated）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `rating_scale` | 上一列 `rating` 的满分。 |

完整参数和字段：<https://everyinfra.com/aliexpress-api/product_detail?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

#### `reviews`（评价）

| 字段 | 含义 |
|---|---|
| `review_id` | 评价 ID。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `rating` | 评分。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `country` | 国家或地区。 |
| `sku_info` | SKU 规格信息（颜色 / 尺寸等组合）。 |
| `helpful_count` | 该评价被标为有用的次数。 |
| `logistics` | 物流方案。 |
| `product_id` | 商品 ID。 |
| `is_anonymous` | 是否匿名评价（reviews）。 |
| `unhelpful_count` | 该评价被标为没帮助的次数（reviews）。 |
| `language` | 内容语言代码（如 zh、en），由平台判定，可能不准。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `rating_scale` | 上一列 `rating` 的满分。 |

完整参数和字段：<https://everyinfra.com/aliexpress-api/reviews?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

#### `variants`（商品变体）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `name` | 名称。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `price` | 价格数值，不含货币符号；币种见 currency。 |
| `original_price` | 原价（划线价）。 |
| `currency` | 价格币种代码（如 CNY、USD）。 |
| `discount` | 折扣力度。 |
| `rating` | 评分。 |
| `review_count` | 评价条数，用于商品/商家类能力。 |
| `shipping` | 运费与配送方式。 |
| `variants` | 规格（SKU）列表，每项一个规格：sku_id、properties（规格名 → 取值，如 Color、Size）、price、original_price、stock、available、image_url、max_buy_count；平台没给的项不出现。 |
| `store_name` | 店铺名称。 |
| `store_url` | 店铺链接。 |
| `image_url` | 图片链接。 |
| `images` | 图片链接：商品类能力里是商品轮播图（按商品页顺序），reviews 里是买家晒图。 |
| `description_images` | 商品描述区图片，来自受限的 AliExpress 媒体正文地址。 |
| `sold_text` | 销量原文（如「10,000+ sold」）；是平台展示的约数，不是精确销量。 |
| `attributes` | 商品属性列表（材质、型号等 {name, value} 行）。 |
| `category_id` | 分类 ID。 |
| `category_path` | 分类路径。 |
| `ship_to` | 这次报价与运费对应的收货国家/地区。 |
| `total_stock` | 商品总库存（各规格合计；单个规格的库存在 variants 每项的 stock）。 |
| `video_url` | 商品视频链接。 |
| `store_id` | 店铺 ID。 |
| `seller_id` | 卖家 ID（速卖通自己的公开 ID）。 |
| `store_country` | 店铺所在国家/地区。 |
| `store_opened_at` | 店铺开设时间。 |
| `store_is_top_rated` | 店铺是否为平台优质卖家（Top Rated）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `rating_scale` | 上一列 `rating` 的满分。 |

完整参数和字段：<https://everyinfra.com/aliexpress-api/variants?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

#### `ratings`（评分汇总）

| 字段 | 含义 |
|---|---|
| `average_star` | 平均星级。 |
| `total_reviews` | 评价总数（写了文字的评价条数；各档星级的条数还算上只打星的，加起来通常更大）。 |
| `positive_rate` | 好评率，百分数（94.1 即 94.1%）。 |
| `negative_rate` | 差评率，百分数。 |
| `five_star` | 打五星的评分，含 count（条数，算上只打星没写字的）；占比 rate 通常没有。 |
| `four_star` | 打四星的评分，含 count。 |
| `three_star` | 打三星的评分，含 count。 |
| `two_star` | 打二星的评分，含 count。 |
| `one_star` | 打一星的评分，含 count。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/aliexpress-api/ratings?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

### 常见问题

**调用时要不要提供速卖通账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $1.39 起。失败、空结果、参数错误和鉴权失败都不收费。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

**能把速卖通接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>。

**用速卖通数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到速卖通的哪些数据？**

速卖通有 6 个能力：关键词搜索、主页或对象详情、商品变体、评价、评分汇总、商品详情。每个能力的参数和返回字段见平台页 <https://everyinfra.com/aliexpress-api?utm_source=github&utm_medium=example_repo&utm_campaign=aliexpress-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 5 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py search "wireless earbuds" --out products.csv` | 2026-11-25 13:22 | 18 | $0.001389 |
| `python main.py product "<商品链接>" --out product.json` | 2026-11-25 13:22 | 1 | $0.001389 |
| `python main.py reviews "<商品链接>" --out reviews.csv` | 2026-11-25 13:23 | 20 | $0.001389 |
| `python main.py variants "<商品链接>" --out variants.csv` | 2026-11-25 13:27 | 1 | $0.001389 |
| `python main.py ratings "<商品链接>" --out ratings.json` | 2026-11-25 15:31 | 1 | $0.001389 |

`product_detail` 返回的一条（正文截到 60 字，作者字段没放进来）：

```json
{
  "id": "3256811621288203",
  "text": "Touch Control Interface\nNavigate your music effortlessly wit…",
  "price": 13.05,
  "original_price": 57.62,
  "currency": "USD",
  "rating": 4.9,
  "review_count": 505,
  "rating_scale": 5
}
```

## License

MIT
