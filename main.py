"""速卖通 API 示例（AliExpress API in Python）。

  python main.py search "wireless earbuds" --out products.csv # 按关键词搜商品 / search products
  python main.py product "<商品链接>" --out product.json      # 商品详情 / product detail
  python main.py reviews "<商品链接>" --out reviews.csv       # 商品评价 / reviews
  python main.py variants "<商品链接>" --out variants.csv     # 规格变体 / variants
  python main.py ratings "<商品链接>" --out ratings.json      # 评分汇总 / rating summary
"""
import argparse

from everyinfra import fetch, report

SORTS = ["popular", "price_asc", "price_desc", "relevance", "top_rated"]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="按关键词搜商品 / search products by keyword")
    s.add_argument("keyword")
    s.add_argument("--sort", choices=SORTS, help="relevance / popular / price_asc / price_desc / top_rated")
    pr = sub.add_parser("product", help="商品详情 / one product")
    pr.add_argument("url")
    r = sub.add_parser("reviews", help="商品评价 / reviews of one product")
    r.add_argument("url")
    r.add_argument("--sort", choices=SORTS, help="newest / relevance")
    v = sub.add_parser("variants", help="商品规格变体 / product variants")
    v.add_argument("url")
    ra = sub.add_parser("ratings", help="评分汇总 / rating summary")
    ra.add_argument("url")
    for x in (s, pr, r, v, ra):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        params = {"keyword": a.keyword, **({"sort": a.sort} if a.sort else {})}
        rows, charged = fetch("search", params)
    elif a.cmd == "product":
        rows, charged = fetch("product_detail", {"url": a.url})
    elif a.cmd == "reviews":
        params = {"url": a.url, **({"sort": a.sort} if a.sort else {})}
        rows, charged = fetch("reviews", params)
    elif a.cmd == "variants":
        rows, charged = fetch("variants", {"url": a.url})
    else:
        rows, charged = fetch("ratings", {"url": a.url})
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
